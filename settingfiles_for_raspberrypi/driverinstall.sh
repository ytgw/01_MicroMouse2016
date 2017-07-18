#!/bin/sh

sudo insmod /home/pi/deviceDriverFromGitHub/lib/Pi2B+/4.9.35-v7+/rtmouse.ko
sudo chmod 666 /dev/rt*
