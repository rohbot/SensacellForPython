#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import sys
import sensalib
import numpy as np
from sensalib.util import *

port = str(sys.argv[1])

#"/dev/ttyUSB1"
s = sensalib.Sensacell(port)
s.fileAddressing("config.txt")
s.setColor(0xFF0000,0,0)
s.fullDisplay()
s.moduleListenning(13)
#s.setColorArray(s.getSensorArray())
#s.fullDisplay()
