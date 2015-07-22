#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import sys
import sensalib
import numpy as np
from sensalib.util import *
import time

port = str(sys.argv[1])

#"/dev/ttyUSB1"
s = sensalib.Sensacell(port)
s.fileAddressing("config.txt")
for i in range (0,20):
	for j in range (0,16):
		s.setColor(0XFF0000,i,j)
"""
for i in range (20,24):
	for j in range (0,8):
		s.setColor(0XFF0000,i,j)
"""
t1 = time.time()
t = s.fullDisplay()
print "intel Display time : ", (time.time() - t1)


while 1:
	s.fullListenning()
	s.setColorArray(s.getSensorArray())
	s.fullDisplay()
	