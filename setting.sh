#! /bin/bash

sudo modprobe w1-gpio
sudo modprobe w1-therm

cat /sys/bus/w1/devices/w1_bus_master1/w1_master_slaves > ./data/sensorname.txt


