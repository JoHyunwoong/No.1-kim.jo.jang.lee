import RPi.GPIO as GPIO
import time

# 변수 이름 마지막이 1이면 소주의 변수이고 2이면 맥주의 변수

def pumpAlcohol(rate, isFirst1, isReplay1, amount_sso, sso_2nd, amount_per_sec_sso, isFirst2, isReplay2, amount_mac, mac_2nd, amount_per_sec_mac):
    speed = 100  # pump speed(pwm)
    sec1 = 0  #소주의 출력시간
    sec2 = 0  #맥주의 출력시간
    # amount_per_sec_sso = 32  # output of sso pump per second
    # amount_per_sec_mac = 28  # output of mac pump per second

    # initialize GPIO
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(12, GPIO.OUT)
    GPIO.output(12, False)
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, False)

    my_pwm = GPIO.PWM(12, 300)
    my_pwm = GPIO.PWM(13, 300)
    my_pwm.start(0)

    my_pwm.ChangeDutyCycle(speed)  # start pwm

    try:

        if (isReplay1 != 1) and (isReplay2 != 1):  #소주와 맥주를 교체하지 않고 다시 실행하는가? 0이면 yes 1이면 no
            if isFirst1 == 1: #소주 실행이 처음인가?(UI 처음 실행할 때 혹은 교체 후에는 값이 1이 됨)
                    sec1 = (180 * rate) / amount_per_sec_sso + 0.65
                    isFirst1 = 0
                    amount_sso -= 180 * rate
            else: #소주 실행이 처음이 아닐 때
                if amount_sso > (180 * rate) * (1 + 0.05):  #남아있는 소주 양이 뽑아야 하는 소주 양보다 많을 때 
                    sec1 = (180 * rate) / amount_per_sec_sso
                    amount_sso -= 180 * rate
                else:  #남아있는 소주 양이 뽑아야 하는 양보다 적어서 교체 후 나머지 양을 마저 뽑아야 할 때 우선 남은 양 전체를 뽑기
                       #교체 후 재실행에서 나머지 양을 마저 뽑도록 isReplay1를 1로 만든다.
                    sec1 = (amount_sso / amount_per_sec_sso) + 0.3
                    sso_2nd = (180 * rate) - amount_sso
                    isReplay1 = 1
                    amount_sso = 0
            if isFirst2 == 1:  #맥주 실행이 처음인가?(UI 처음 실행할 때 혹은 교체 후에는 값이 1이 됨)
                    sec2 = (180 * (1 - rate)) / amount_per_sec_mac + 1 + 1.9
                    isFirst2 = 0
                    amount_mac -= (180 * (1 - rate))
            else:  #맥주 실행이 처음이 아닐 때
                if amount_mac > (180 * (1 - rate)) * (1 + 0.05):
                    sec2 = (180 * (1 - rate)) / amount_per_sec_mac + 1 + 1.7
                    amount_mac -= (180 * (1 - rate))
                else:   #남아있는 맥주 양이 뽑아야 하는 양보다 적어서 교체 후 나머지 양을 마저 뽑아야 할 때 우선 남은 양 전체를 뽑기
                       #교체 후 재실행에서 나머지 양을 마저 뽑도록 isReplay2를 1로 만든다.
                    sec2 = (amount_mac / amount_per_sec_mac) + 0.5 + 1.9
                    mac_2nd = (180 * (1 - rate)) - amount_mac
                    isReplay2 = 1
                    amount_mac = 0

            # pump output
            GPIO.output(12, True)
            GPIO.output(13, True)

            time.sleep(sec1)
            GPIO.output(12, False)

            time.sleep(sec2 - sec1)
            GPIO.output(13, False)

            GPIO.cleanup()

            return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd

        if (isReplay1 == 1) and (isReplay2 == 1) :    #소주와 맥주 둘 다 교체한 후 처음 실행이라면
            sec1 = (sso_2nd / amount_per_sec_sso) + 0.8
            sec2 = (mac_2nd / amount_per_sec_mac) + 1.3

            if sec2 >= sec1:  # 맥주 출력시간이 소주 출력시간보다 클 경우의 gpio 출력
                # pump output
                GPIO.output(12, True)
                GPIO.output(13, True)

                time.sleep(sec1)
                GPIO.output(12, False)

                time.sleep(sec2 - sec1)
                GPIO.output(13, False)

                GPIO.cleanup()

                isReplay1 = 0
                isFirst1 = 1
                isReplay2 = 0
                isFirst2 = 1
        
                amount_sso -= (sec1 - 0.8) * amount_per_sec_sso
                amount_mac -= (sec2 - 1.3) * amount_per_sec_mac

                return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd

            else:   # 맥주 출력시간이 소주 출력시간보다 작을 경우의 gpio 출력
            
                # pump output
                GPIO.output(12, True)
                GPIO.output(13, True)

                time.sleep(sec2)
                GPIO.output(13, False)

                time.sleep(sec1 - sec2)
                GPIO.output(12, False)

                GPIO.cleanup()

                isReplay1 = 0
                isFirst1 = 1
                isReplay2 = 0
                isFirst2 = 1
        
                amount_sso -= (sec1 - 0.8) * amount_per_sec_sso
                amount_mac -= (sec2 - 1.3) * amount_per_sec_mac

                return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd

        if (isReplay1 == 1) and (isReplay2 != 1) :    #소주만 교체한 후 처음 실행이라면
            sec1 = (sso_2nd / amount_per_sec_sso) + 0.8

            # pump output
            GPIO.output(12, True)
            time.sleep(sec1)
            GPIO.output(12, False)
            GPIO.cleanup()

            isReplay1 = 0
            isFirst1 = 1
        
            amount_sso -= (sec1 - 0.8) * amount_per_sec_sso

            return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd

        if (isReplay1 != 1) and (isReplay2 == 1) :   #맥주만 교체한 후 처음 실행이라면
            sec2 = (sso_2nd / amount_per_sec_sso) + 1.3

            # pump output
            GPIO.output(13, True)
            time.sleep(sec2)
            GPIO.output(13, False)
            GPIO.cleanup()

            isReplay2 = 0
            isFirst2 = 1
        
            amount_mac -= (sec2 - 1.3) * amount_per_sec_mac

            return isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd

    except:
            return 0
