import RPi.GPIO as GPIO
import time

def pumpSso(rate, isFirst, isReplay, amount_sso, sso_2nd, amount_per_sec_sso):
    speed = 100  # pump speed(pwm)
    sec = 0  # total sec of sso
    # amount_per_sec_sso = 32  # output of sso pump per second

    # initialize GPIO
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(12, GPIO.OUT)
    GPIO.output(12, False)

    my_pwm = GPIO.PWM(12, 300)
    my_pwm.start(0)

    my_pwm.ChangeDutyCycle(speed)  # start pwm

    if isReplay != 1:
        if isFirst == 1:
                sec = (180 * rate) / amount_per_sec_sso + 0.8
                isFirst = 0
        else:
            if amount_sso > (180 * rate) * (1 + 0.05):
                sec = (180 * rate) / amount_per_sec_sso
            else:    # 뽑아야 하는 양보다 남은 양이 적을 때 우선 남은 양만 뽑기
                sec = (amount_sso / amount_per_sec_sso) + 0.5
                sso_2nd = (180 * rate) - amount_sso
                isReplay = 1

        # pump output
        GPIO.output(12, True)
        time.sleep(sec)

        GPIO.output(12, False)

        GPIO.cleanup()

        return isFirst, isReplay, amount_sso, sso_2nd   # isReplay = 1 => UI 병체 알림

    else:    # (뽑아야 하는 양 - 남은 양)을 마저 뽑기
        sec = (sso_2nd / amount_per_sec_sso) + 0.8

        # pump output
        GPIO.output(12, True)
        time.sleep(sec)
        GPIO.output(12, False)
        GPIO.cleanup()

        isReplay = 0
        isFirst = 1

        return isFirst, isReplay, amount_sso, sso_2nd

        
