#!/bin/sh

sudo insmod /home/pi/RaspberryPiMouse/lib/Pi2B+/4.4.13-v7+/rtmouse.ko
lsmod | grep rtmouse
sudo chmod 666 /dev/rt*