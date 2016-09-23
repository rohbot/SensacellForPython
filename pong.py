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

def setColor(color):
	for i in range(8):
		for j in range(8):
			s.setColor(i,j,color)

	s.fullDisplay()

def drawPaddle(pos,color):
	if color == RED:
		y = 0
	if color == BLUE:
		y = 7	
	for i in range(8):
		if i == pos:
			s.setColor(y,i, color)
		else:
			s.setColor(y,i, BLACK)
	
	s.setColor(y,pos-1, color)
	s.setColor(y,pos+1, color)
		
	if pos == 0:
		s.setColor(y,1, color)
		s.setColor(y,2, color)
	if pos == 7:
		s.setColor(y,6, color)
		s.setColor(y,5, color)
		
				

setColor(BLACK)
time.sleep(0.1)

prev_red = []
prev_blue = []
red_pos = 4
blue_pos = 4
while 1 :
	s.fullListenning()
	b = s.getSensorArray()
	# for i in range(len(b)):
	# 	for j in range(len(b[i])):
	# 		if b[i][j] > 0:
	# 			#print i,j
	red_row = b[0]
	blue_row = b[7]
	if not np.array_equal(red_row, prev_red):
		prev_red = red_row
		val = 0
		print red_row
		for i in range(len(red_row)):
			#print i, red_row[i]
			if red_row[i] > val:
				val = red_row[i]
				red_pos = i
		drawPaddle(red_pos,RED)
		s.fullDisplay()
	
	if not np.array_equal(blue_row, prev_blue):
		prev_blue = blue_row
		val = 0
		print blue_row
		for i in range(len(red_row)):
			#print i, red_row[i]
			if blue_row[i] > val:
				val = blue_row[i]
				blue_pos = i
		drawPaddle(blue_pos,BLUE)
		
		
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