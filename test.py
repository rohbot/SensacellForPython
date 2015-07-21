#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import sensalib
import numpy as np
from sensalib.util import *

s = sensalib.Sensacell("/dev/ttyUSB0")

s.setSerial("/dev/ttyUSB0")

s.autoAddressing("config.txt")

s.fileAddressing("config.txt")








"""
s.write("0101a01\r");
color = 0x0000
fourtab = np.full((4,4), color)
fourtab[3,3] = 0xFFFFFF
fourtab[2,2] = 0xFFFF
for line in fourtab:
	for element in line:
		s.write(util.intToByte(element))
"""
