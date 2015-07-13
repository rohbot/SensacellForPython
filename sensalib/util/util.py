#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

def intToByte(integer):
	string = "%0.6X"%integer
	return string.decode("hex")