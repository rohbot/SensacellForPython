#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import sys
import sensalib
import numpy as np
from sensalib.util import *
import time
import redis

#port = str(sys.argv[1])

#"/dev/ttyUSB1"
r = redis.Redis()

s = sensalib.Sensacell() #"/dev/ttyUSB0")
s.fileAddressing("config.txt")
#s.setBinaryMode()
#s.setTrigger(1)

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
	if quad == 0:
		for i in range(4):
			for j in range(4):
				s.setColor(i,j,color)
	if quad == 3:
		for i in range(4,8):
			for j in range(4):
				s.setColor(i,j,color)
	if quad == 1:
		for i in range(4):
			for j in range(4,8):
				s.setColor(i,j,color)
	if quad == 2:
		for i in range(4,8):
			for j in range(4,8):
				s.setColor(i,j,color)
	
def sendQuad(quads):				
	r.publish('quad',quads)

#delay = 0.1


#setColor(BLACK)
#time.sleep(delay)
prev_quad = [0,0,0,0]
quad_colours = [RED,BLUE,YELLOW,GREEN]
while 1 :
	s.fullListenning()
	quad_on = [0,0,0,0]
	b = s.getSensorArray()
	for i in range(len(b)):
		for j in range(len(b[i])):
			if b[i][j] > 0:
				#print i,j
				if i > 4:
					if j > 4:
						quad_on[2] = 1 
					else:
						quad_on[3] = 1
				else:
					if j > 4:
						quad_on[1] = 1
					else:
						quad_on[0] = 1

	#print quad_on
	if prev_quad != quad_on:
		
		prev_quad = quad_on	
		sendQuad(quad_on)				
		for i in range(4):
			if quad_on[i]:
				colorQuadrant(i,quad_colours[i])
			else:
				colorQuadrant(i,BLACK)
		s.fullDisplay()

	#sensor =0x0000FF * np.array(b)
	print b
	#s.setColorArray(sensor)
	#s.fullDisplay()
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