#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import serial
import time

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=230400,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

if ser.isOpen():
	print "port OPEN "

#print ser


#13EAa00
ser.write("13EAa00")
ser.write("\r")

i = 0

while i < 35 :
	print ser.read(20)
	i += 1