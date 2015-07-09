#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import serial
import time
import numpy as np

class Sensacell:

	def __init__(self, port):
		self.nqme = "sensqcell"
		self.__name = "Sensacell"
		self.__serUSB = serial.Serial(
			port,
			#port ='/dev/ttyUSB0'
			baudrate=230400,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)

	def Init(self):
		self.__serUSB.write("13EAa00\r")
		time.sleep(0.8)

	def write(self, str):
		self.__serUSB.write(str + "\r")