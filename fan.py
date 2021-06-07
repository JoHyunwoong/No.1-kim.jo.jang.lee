import RPi.GPIO as GPIO
import time
import os
import pigpio

# Setting
GPIO.setmode(GPIO.BCM)

fan_GPIO_num = 21 # wPi 29

def read_temp():
    f = open("../data/temperature.txt", 'r')
    s = f.readline()
    f.close()
    return s

# Determine fan pwm value
def det_fan_pwm(temp, target_temp):
    print(target_temp)
    if((temp - target_temp) > 20):
        return 0.01
    else:
        return abs(temp - target_temp)/2000


def fan_main(q, t):
    target_temp = 6
    while True:
        temp = q.get()
        if not t.empty():
            target_temp = t.get()
        pwm = det_fan_pwm(temp, target_temp)
        GPIO.output(fan_GPIO_num, 1)
        time.sleep(pwm)
        GPIO.output(fan_GPIO_num, 0)
        time.sleep(0.01 - pwm)
