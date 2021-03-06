#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import sys
import sensalib
import numpy as np
from sensalib.util import *
import time

#port = str(sys.argv[1])

#"/dev/ttyUSB1"
s = sensalib.Sensacell() #"/dev/ttyUSB0")
s.fileAddressing("config.txt")
s.setProportionnalMode()
s.setTrigger(1)

RED = 0xFF0000
BLUE = 0x0000FF
GREEN = 0x00FF00
YELLOW = 0xFFFF00
BLACK = 0x000000


def setColor(color):
	for i in range(8):
		for j in range(8):
			s.setColor(i,j,color)

	s.fullDisplay()

def colorQuadrant(quad,color):
	if quad == 1:
		for i in range(4):
			for j in range(4):
				s.setColor(i,j,color)
	if quad == 4:
		for i in range(4,8):
			for j in range(4):
				s.setColor(i,j,color)
	if quad == 2:
		for i in range(4):
			for j in range(4,8):
				s.setColor(i,j,color)
	if quad == 3:
		for i in range(4,8):
			for j in range(4,8):
				s.setColor(i,j,color)
	
				
	s.fullDisplay()


while 1:
	colorQuadrant(1, RED)
	colorQuadrant(2, BLUE)
	colorQuadrant(3, GREEN)
	colorQuadrant(4, YELLOW)

	time.sleep(1)

	colorQuadrant(2, RED)
	colorQuadrant(3, BLUE)
	colorQuadrant(4, GREEN)
	colorQuadrant(1, YELLOW)

	time.sleep(1)

	colorQuadrant(3, RED)
	colorQuadrant(4, BLUE)
	colorQuadrant(1, GREEN)
	colorQuadrant(2, YELLOW)

	time.sleep(1)

	colorQuadrant(4, RED)
	colorQuadrant(1, BLUE)
	colorQuadrant(2, GREEN)
	colorQuadrant(3, YELLOW)

	time.sleep(1)

	setColor(BLACK)
	time.sleep(1)


while 1 :
	s.fullListenning()
	b = s.getSensorArray()
	# for i in range(len(b)):
	# 	for j in range(len(b[i])):
	# 		if b[i][j] > 0:
	# 			print i,j

	#sensor =0x0000FF * np.array(b)
	print b
	#s.setColorArray(sensor)
	#s.fullDisplay()
	time.sleep(1)

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