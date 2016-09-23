#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import sys
import sensalib
import numpy as np
from sensalib.util import *
import time
import redis

RED = 0xFF0000
BLUE = 0x0000FF
GREEN = 0x00FF00
YELLOW = 0xFFFF00
BLACK = 0x000000

r = redis.Redis()

s = sensalib.Sensacell() 
s.fileAddressing("config.txt")
s.setProportionnalMode()
s.setTrigger(1)

last_changed = []


def setColor(color):
	for i in range(8):
		for j in range(8):
			s.setColor(i,j,color)

	s.fullDisplay()

def morphColor(color):
	red_part =  (color & 0xFF0000) 
	blue_part = (color & 0x0000FF) 

	if red_part > 0:
		red_part -= 1
		red_part = red_part & 0xFF0000
	if blue_part < 255:
		red_part += 1
	color = (red_part) + blue_part		
	return color

setColor(BLUE)
time.sleep(0.1)

for i in range(8):
	a = []
	for j in range(8):
		a.append(time.time())
	last_changed.append(a)

while 1 :
	s.fullListenning()
	b = s.getSensorArray()
	c = s.getColorArray()
	for i in range(len(b)):
		for j in range(len(b[i])):
			if b[i][j] > 10 and time.time() - last_changed[i][j] > 1:
				#print time.time() - last_changed[i][j], b[i][j]
				#color = c[i][j]
				s.setColor(i,j,RED)

				last_changed[i][j] = time.time()

			if c[i][j] != BLUE and time.time() - last_changed[i][j] > 0.02:
				color = morphColor(int(c[i][j]))
				s.setColor(i,j,color)
				last_changed[i][j] = time.time()



				
	s.fullDisplay()
	#time.sleep(1)

"""
s.setColorArray(np.zeros((24,16)))
t1 = time.time()
s.setCircle(5,8,8,0x0000FF)
print s.getColorArray()
#sensalib.util.drawCircle(s.getColorArray(), 8,8,8,0xFF0000)
print "->", time.time() - t1
s.fullDisplay()
#s.moduleDisplay(16)
#s.moduleDisplay(12)

while 1:
	s.update()
	b = s.getSensorArray()
	sensor = 1114112*np.array(b)
	s.setColorArray(sensor)
	centroids = s.getSensorsCentroids()
	for centroid in centroids:
		s.setColor(centroid[1],centroid[0],0xFF0000)

"""