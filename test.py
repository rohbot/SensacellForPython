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
	s.fullListenning()
	b = s.getSensorArray()
	sensor = (0x00FF00/30)*np.array(b)
	
	s.setColorArray(sensor)
	s.fullDisplay()