#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import sys
import sensalib
import numpy as np
from sensalib.util import *
import time
import redis
import serial

RED = 0xFF0000
BLUE = 0x0000FF
GREEN = 0x00FF00
YELLOW = 0xFFFF00
BLACK = 0x000000

r = redis.Redis()

strPort = '/dev/ttyACM0'

ser = serial.Serial(strPort, 115200)



s = sensalib.Sensacell() 
s.fileAddressing("config.txt")
s.setProportionnalMode()
s.setTrigger(1)

colours = [RED,BLUE,GREEN,YELLOW]

def setColor(color):
	for i in range(8):
		for j in range(8):
			s.setColor(i,j,color)

	s.fullDisplay()

setColor(BLACK)
time.sleep(0.1)


def setLEDColor(color):
	ser.write(str(color))

def check_touch(sensor_array):
	touched = False
	for i in range(len(sensor_array)):
		for j in range(len(sensor_array[i])):
			if sensor_array[i][j] > 10:
				#print i,j, sensor_array[i][j] , time.time()
				return True
	return touched

def fadeColor(color):
	red_part =  (color & 0xFF0000) 
	green_part = (color & 0x00FF00)
	blue_part = (color & 0x0000FF) 

	if red_part > 0:
		red_part -= 1
		red_part = red_part & 0xFF0000
	if green_part > 0:
		green_part -= 1
		green_part = green_part & 0x00FF00
	if blue_part > 0:
		blue_part -= 1
	color = red_part + green_part + blue_part
	#print red_part, green_part, blue_part		
	return color



last_changed = time.time()

current_colour = BLACK
while 1 :
	s.fullListenning()
	b = s.getSensorArray()
	c = s.getColorArray()

	if check_touch(b) and time.time() - last_changed > 2:
		if current_colour == RED:
			current_colour = BLUE
		elif current_colour == BLUE:
			current_colour = GREEN
		elif current_colour == GREEN:
			current_colour = YELLOW
		else:
			current_colour = RED
		
		setColor(current_colour)
		setLEDColor(current_colour)
		#print current_colour
		last_changed = time.time()
	

		dim_color = current_colour
		while dim_color > 0:
			dim_color= fadeColor(dim_color)
			setColor(dim_color)
			time.sleep(0.001)
		print time.time() - last_changed
		setLEDColor(BLACK)
		time.sleep(0.5)	
