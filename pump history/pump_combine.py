import RPi.GPIO as GPIO
import time

# 변수 이름 마지막이 1이면 소주의 변수이고 2이면 맥주의 변수
# rate = 비율(소주양/전체양)
# isFirst1, 2 = 1은 소주의 출력이 처음인가? 혹은 교체 후인가? 1이면 yes, 1이 아니면 no 2는 똑같이 맥주에 대한 것
# isReplay1, 2 = 소주 혹은 맥주의 병을 교체한 후 처음 실행인가? 1이면 yes 1이 아니면 no
# amount_sso, amount_mac = 순서대로 각각 소주, 맥주의 남은 양
# sso_2nd, mac_2nd = 순서대로 각각 소주, 맥주의 병 교체 후 실행시 직전 실행에서 부족했던 양을 마저 뽑아야 하는 양
# amount_per_sec_sso, amount_per_sec_mac = 순서대로 각각 소주와 맥주 펌프의 시간당 출력양
# isError = 1일 때는 소주병을 교체하라는 의미, 2는 맥주병을 교체, 나머지 3~6은 리턴값을 주기 위해 할당한 것으로 의미를 지니지는 않음
# try-except에서 에러시 7을 9개 리턴

def pumpAlcohol(rate, isFirst1, isReplay1, amount_sso, sso_2nd, amount_per_sec_sso, isFirst2, isReplay2, amount_mac, mac_2nd, amount_per_sec_mac):
	speed = 100  # pump speed(pwm)
	isError = 0
	print(1)
	sec1 = 0  
	sec2 = 0  
	# amount_per_sec_sso = 32  # output of sso pump per second
	# amount_per_sec_mac = 28  # output of mac pump per second

	# initialize GPIO
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(1, GPIO.OUT)
	GPIO.output(1, False)
	GPIO.setup(6, GPIO.OUT)
	GPIO.output(6, False)
	'''
	my_pwm = GPIO.PWM(12, 300)
	my_pwm = GPIO.PWM(13, 300)
	my_pwm.start(0)
    
	my_pwm.ChangeDutyCycle(speed)  # start pwm
	'''
	try:

		if (isReplay1 != 1) and (isReplay2 != 1):  
			if isFirst1 == 1:
				if rate == 0.0:
					se1 = 0
				else:  
					sec1 = (180 * rate) / amount_per_sec_sso + 0.5
				isFirst1 = 0
				amount_sso -= 180 * rate
			else:  
				if amount_sso > (180 * rate) * (1 + 0.1):  
					if rate == 0.0:
						se1 = 0
					else:
						sec1 = (180 * rate) / amount_per_sec_sso
					amount_sso -= 180 * rate
				else:  
					if rate == 0.0:
						se1 = 0
					else:
						sec1 = (amount_sso / amount_per_sec_sso) + 0.5
					sso_2nd = (180 * rate) - amount_sso
					isReplay1 = 1
					amount_sso = 0
					isError = 1
			if isFirst2 == 1:  
				if rate == 1.0:
					sec2 = 0
				else:
					sec2 = (180 * (1 - rate)) / amount_per_sec_mac + 1 + 1.1
				isFirst2 = 0
				amount_mac -= (180 * (1 - rate))
			else:  
				if amount_mac > (180 * (1 - rate)) * (1 + 0.1):
					if rate == 1.0:
						sec2 = 0
					else:
						sec2 = (180 * (1 - rate)) / amount_per_sec_mac + 1 + 1.1
					amount_mac -= (180 * (1 - rate))
				else:  
					if rate == 1.0:
						sec2 = 0
					else:
						sec2 = (amount_mac / amount_per_sec_mac) + 0.5 + 1.9
					mac_2nd = (180 * (1 - rate)) - amount_mac
					isReplay2 = 1
					amount_mac = 0
					isError = 2
			if sec2 >= sec1:
				# pump output
				GPIO.output(1, True)
				GPIO.output(6, True)

				time.sleep(sec1)
				GPIO.output(1, False)

				time.sleep(sec2 - sec1)
				GPIO.output(6, False)
				GPIO.cleanup()

				return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd, isError
			else: 
				# pump output
				GPIO.output(6, True)
				GPIO.output(1, True)

				time.sleep(sec2)
				GPIO.output(6, False)

				time.sleep(sec1 - sec2)
				GPIO.output(1, False)
				GPIO.cleanup()

				return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd, isError

		if (isReplay1 == 1) and (isReplay2 == 1):  
			sec1 = (sso_2nd / amount_per_sec_sso) + 0.5
			sec2 = (mac_2nd / amount_per_sec_mac) + 1 + 1.1

			if sec2 >= sec1:  
				# pump output
				GPIO.output(1, True)
				GPIO.output(6, True)

				time.sleep(sec1)
				GPIO.output(1, False)

				time.sleep(sec2 - sec1)
				GPIO.output(6, False)
				GPIO.cleanup()

				isReplay1 = 0
				isFirst1 = 1
				isReplay2 = 0
				isFirst2 = 1
				isError = 3

				amount_sso -= (sec1 - 0.5) * amount_per_sec_sso
				amount_mac -= (sec2 - 2.1) * amount_per_sec_mac

				return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd, isError

			else:  

				# pump output
				GPIO.output(6, True)
				GPIO.output(1, True)

				time.sleep(sec2)
				GPIO.output(6, False)

				time.sleep(sec1 - sec2)
				GPIO.output(1, False)

				GPIO.cleanup()

				isReplay1 = 0
				isFirst1 = 1
				isReplay2 = 0
				isFirst2 = 1
				isError = 4

				amount_sso -= (sec1 - 0.5) * amount_per_sec_sso
				amount_mac -= (sec2 - 2.1) * amount_per_sec_mac

				return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd, isError

		if (isReplay1 == 1) and (isReplay2 != 1):  
			sec1 = (sso_2nd / amount_per_sec_sso) + 0.5

			# pump output
			GPIO.output(1, True)
			time.sleep(sec1)
			GPIO.output(1, False)
			GPIO.cleanup()

			isReplay1 = 0
			isFirst1 = 1
			isError = 5

			amount_sso -= (sec1 - 0.5) * amount_per_sec_sso

			return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd, isError

		if (isReplay1 != 1) and (isReplay2 == 1):  
			sec2 = (sso_2nd / amount_per_sec_sso) + 1 + 1.1

			# pump output
			GPIO.output(6, True)
			time.sleep(sec2)
			GPIO.output(6, False)
			GPIO.cleanup()

			isReplay2 = 0
			isFirst2 = 1
			isError = 6

			amount_mac -= (sec2 - 2.1) * amount_per_sec_mac

			return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd, isError

	except:
		return 7, 7, 7, 7, 7, 7, 7, 7, 7
