#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

from skimage.draw import circle
from skimage.draw import circle_perimeter

def intToByte(integer):
	string = "%0.6X"%integer
	return string.decode("hex")