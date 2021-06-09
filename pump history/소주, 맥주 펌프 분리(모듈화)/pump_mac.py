import RPi.GPIO as GPIO
import time

def pumpMac(rate, isFirst2, isReplay2, amount_mac, mac_2nd, amount_per_sec_mac):
    speed = 100  # pump speed(pwm)
    sec = 0  # total sec of mac
    # amount_per_sec_mac = 28  # output of mac pump per second

    # initialize GPIO
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, False)

    my_pwm = GPIO.PWM(13, 300)
    my_pwm.start(0)

    my_pwm.ChangeDutyCycle(speed)  # start pwm

    if isReplay2 != 1:
        if isFirst2 == 1:
                sec = (180 * (1 - rate)) / amount_per_sec_mac + 1.3
                isFirst2 = 0
                amount_mac -= (180 * (1 - rate))
        else:
            if amount_mac > (180 * (1 - rate)) * (1 + 0.05):
                sec = (180 * (1 - rate)) / amount_per_sec_mac
                amount_mac -= (180 * (1 - rate))
            else:    # 뽑아야 하는 양보다 남은 양이 적을 때 우선 남은 양만 뽑기
                sec = (amount_mac / amount_per_sec_mac) + 0.5
                mac_2nd = (180 * (1 - rate)) - amount_mac
                isReplay2 = 1
                amount_mac = 0

        # pump output
        GPIO.output(13, True)
        time.sleep(sec)

        GPIO.output(13, False)

        GPIO.cleanup()

        return isFirst2, isReplay2, amount_mac, mac_2nd    # isReplay = 1 => UI 병체 알림

    else:   # (뽑아야 하는 양 - 남은 양)을 마저 뽑기
        sec = (mac_2nd / amount_per_sec_mac) + 1.3

        # pump output
        GPIO.output(13, True)
        time.sleep(sec)
        GPIO.output(13, False)
        GPIO.cleanup()

        isReplay2 = 0
        isFirst2 = 1
        
        amount_mac -= (sec - 1.3) * amount_per_sec_mac

        return isFirst2, isReplay2, amount_mac, mac_2nd
