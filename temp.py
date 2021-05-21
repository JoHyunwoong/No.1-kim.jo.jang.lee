'''
사전 순서: 1. 명령창에 sudo modprobe w1-gpio && sudo modprode w1_therm 
          2. 명령창에 sudo nano /boot/config.text (config.text 파일 열기 위함)
          3. config.text 파일 마지막에 dtoverlay = w1-gpio 추가
          4. 명령창에 ls -l /sys/bus/w1/devices/ 친 후 장치 주소 확인(28-00000xxxxx)
'''
      

import time


def displayTemp():

    tempFile = open("/sys/bus/w1/devices/장치 주소(사전 순서 3)/w1_slave")
    theText = tempFile.read()
    tempFile.close()
    tempDate = theText.split("\n")[1].split(" ")[9]
    temperature = float(tempData[2:])
    temperature = temperature / 1000

    return temperature
