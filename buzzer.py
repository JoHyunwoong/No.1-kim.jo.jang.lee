import time
import RPi.GPIO as GPIO


def buzzer():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)

    GPIO.output(26, True)
    time.sleep(1)
    GPIO.cleanup()
