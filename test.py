#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import sensalib
import numpy as np

s = sensalib.Sensacell("/dev/ttyUSB0")
s.write("13EAa00")