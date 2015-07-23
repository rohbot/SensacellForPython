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
s.setProportionnalMode()
s.setTrigger(1)


while 1:
	s.update()
	b = s.getSensorArray()
	sensor = 1114112*np.array(b)
	s.setColorArray(sensor)
