import RPi.GPIO as GPIO
import time


def pumpAlcohol(rate, amount_sso, amount_mac):

    speed = 100  #pump speed(pwm)
    sec1 = 0   #total sec of sso
    sec2 = 0   #total sec of mac
    amount_per_sec = 5 # output of pump per second

    if (amount_sso > 360 * 0.05) and (amount_mac > 500 * 0.05):

        try:
            # initialize GPIO
            GPIO.setmode(GPIO.BCM)

            GPIO.setup(23, GPIO.OUT)
            GPIO.output(23, False)

            GPIO.setup(24, GPIO.OUT)
            GPIO.output(24, False)

            my_pwm = GPIO.PWM(23, 300)
            my_pwm = GPIO.PWM(24, 300)
            my_pwm.start(0)

            my_pwm.ChangeDutyCycle(speed) #start pwm

            sec1 = (180 * rate) / amount_per_sec
            sec2 = (180 * (1 - rate)) / amount_per_sec

            # pump output
            GPIO.output(23, True)
            GPIO.output(24, True)
            time.sleep(sec1)

            GPIO.output(23, False)

            time.sleep(sec2 - sec1)
            GPIO.output(24, False)

            GPIO.cleanup()

            amount_sso -= sec1 * amount_per_sec
            amount_mac -= sec2 * amount_per_sec

            if amount_sso < 0:
                amount_sso = 0
            if amount_mac < 0:
                amount_mac = 0

            return 0, amount_sso, amount_mac

        except:
            return 1, amount_sso, amount_mac

    else:
        return 2, amount_sso, amount_mac  # display 'amount shortage' in UI