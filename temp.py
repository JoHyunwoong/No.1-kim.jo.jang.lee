import time


def displayTemp():

    tempFile = open("/sys/bus/w1/devices/(센서 주소)/w1_slave")
    theText = tempFile.read()
    tempFile.close()
    tempDate = theText.split("\n")[1].split(" ")[9]
    temperature = float(tempData[2:])
    temperature = temperature / 1000

    return temperature
