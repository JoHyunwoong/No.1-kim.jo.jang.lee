import RPi.GPIO as GPIO
import time


def buzzer():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    scale1 = [1000]
    scale2 = [956, 1014, 1136]

    p = GPIO.PWM(16, 100)
    p.start(0)
    p.ChangeDutyCycle(50)

    for i in range(len(scale1)):
        p.ChangeFrequency(scale2[i])
        time.sleep(1)

    p.stop()

    GPIO.cleanup()


if __name__ == "__main__":
    buzzer()