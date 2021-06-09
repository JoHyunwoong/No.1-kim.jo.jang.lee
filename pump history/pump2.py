import RPi.GPIO as GPIO
import time


def pumpAlcohol(rate, amount_sso, amount_mac, isFirst):
    speed = 100  # pump speed(pwm)
    sec1 = 0  # total sec of sso
    sec2 = 0  # total sec of mac
    amount_per_sec_mac = 28  # output of mac pump per second
    amount_per_sec_sso = 32  # output of sso pump per second

    if (amount_sso > 360 * 0.05) and (amount_mac > 500 * 0.05):
        try:
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

            if isFirst == 1:
                sec1 = (180 * rate) / amount_per_sec_sso + 0.8
                sec2 = (180 * (1 - rate)) / amount_per_sec_mac + 1.3
            else:
                sec1 = (180 * rate) / amount_per_sec_sso
                sec2 = (180 * (1 - rate)) / amount_per_sec_mac

            amount_sso -= (180 * rate)
            amount_mac -= (180 * (1 - rate))

            if (amount_sso >= 360 * 0.05) and (amount_mac < 0):
                amount_mac = 0
                return 3, amount_sso, amount_mac  # display 'amount shortage' in UI

            elif (amount_sso < 360 * 0.05) and (amount_mac < 0):
                amount_sso = 0
                amount_mac = 0
                return 4, amount_sso, amount_mac  # display 'amount shortage' in UI

            elif (amount_sso < 0) and (amount_mac >= 500 * 0.05):
                amount_sso = 0
                return 5, amount_sso, amount_mac  # display 'amount shortage' in UI

            elif (amount_sso < 0) and (amount_mac < 500 * 0.05):
                amount_sso = 0
                amount_mac = 0
                return 6, amount_sso, amount_mac  # display 'amount shortage' in UI

            # pump output
            GPIO.output(12, True)
            GPIO.output(13, True)
            time.sleep(sec1)

            GPIO.output(12, False)

            time.sleep(sec2 - sec1)
            GPIO.output(13, False)

            GPIO.cleanup()

            return 0, amount_sso, amount_mac

        except:
            return 1, amount_sso, amount_mac

    else:
        return 2, amount_sso, amount_mac  # display 'amount shortage' in UI
