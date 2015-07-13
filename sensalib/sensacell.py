#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import util
import serial
import time
import numpy as np

class Sensacell:

	def __init__(self, port):
		self.__name = "Sensacell"
		self.__serUSB = serial.Serial(
			port,
			#port ='/dev/ttyUSB0'
			baudrate=230400,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)
		self.__virtualArray = np.zeros((24,16))

	def init(self):
		self.__serUSB.write("13EAa00\r")
		time.sleep(0.01)

	def autoAddressing(self, filename):
		AddressList = {}
		self.__serUSB.flushOutput()
		self.__serUSB.write("13EAa00\r")
		i = 0
		while i <= 34:
			print self.__serUSB.readline(20)
			i+=1

	def write(self, str):
		self.__serUSB.flushInput()
		self.__serUSB.write(str)

	def array(self):
		return self.__virtualArray