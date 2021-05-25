import RPi.GPIO as GPIO
import time
import os

# Setting for GPIO
GPIO.setmode(GPIO.BCM)

# GPIO ports for the 7seg pins
# A, B, C, D, E, F, G, DP
segments = (26, 5, 27, 23, 24, 19, 18, 22)

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

# GPIO ports for the digit 0-3 pins
digits = (12, 13, 6, 17)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

num = {' ': (0, 0, 0, 0, 0, 0, 0),
        '0' : (1, 1, 1, 1, 1, 1, 0),
        '1' : (0, 1, 1, 0, 0, 0 ,0),
        '2' : (1, 1, 0, 1, 1, 0, 1),
        '3' : (1, 1, 1, 1, 0, 0, 1),
        '4' : (0, 1, 1, 0, 0, 1, 1),
        '5' : (1, 0, 1, 1, 0, 1, 1),
        '6' : (1, 0, 1, 1, 1, 1, 1),
        '7' : (1, 1, 1, 0, 0, 0, 0),
        '8' : (1, 1, 1, 1, 1, 1, 1),
        '9' : (1, 1, 1, 1, 0, 1, 1)}

# Read temperature
def read_temp():
    f = open("../data/temperature.txt", 'r')
    s = f.readline()
    f.close()
    s = s.replace('.', '')
    if(len(s) < 4):
        s += "0000"
    return s

try:
    while(True):
        s = read_temp()
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[s[digit]][loop])
#           GPIO.output(digits[digit], 1)
            if(digit == 1):
                GPIO.output(22, 1)
            else:
                GPIO.output(22, 0)
            GPIO.output(digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(digits[digit], 1)
            time.sleep(0.001)
finally:
    GPIO.cleanup()
