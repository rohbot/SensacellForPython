#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import util
import serial
import time
import numpy as np
import io
import pickle

class Sensacell:

	def __init__(self, port):
		self.__name = "Sensacell"
		self.__serUSB = serial.Serial(
			port,
			#port ='/dev/ttyUSB0',
			baudrate=230400,
			bytesize=serial.EIGHTBITS,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			timeout = 10
		)
		self._ser = io.TextIOWrapper(io.BufferedRWPair(self.__serUSB,self.__serUSB,1),
							newline = '\r',
							line_buffering = True)
		self.__colorArray = []
		self.__sensorArray = []
		self.__addressList = {}
		self.__height = 0
		self.__width = 0

	def setSerial(self, port):
		self.__serUSB = serial.Serial(
			port,
			#port ='/dev/ttyUSB0',
			baudrate=230400,
			bytesize=serial.EIGHTBITS,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			timeout = 10
		)
		self._ser = io.TextIOWrapper(io.BufferedRWPair(self.__serUSB,self.__serUSB,1),
							newline = '\r',
							line_buffering = True)

	def autoAddressing(self, filename):
		print "autoAddressing..."
		self.__addressList = {}
		self.__write("13EAa00\r")
		line = ""
		while line != "01b00\r":
			line = self._ser.readline()
			if len (line) == 9:
				if line[:1]=='0' or line[:1]=='1':
					x=4*(int(line[4:6],16)-1)
					y=4*(int(line[2:4],16)-1)
					if x/4 > self.__width :
						self.__width = x/4 + 1
					if y/4 > self.__height :
						self.__height = y/4 + 1
					self.__addressList[int(line[6:8],16)] = [x,y]

		self.__colorArray = np.zeros((self.__height*4, self.__width*4))
		self.__sensorArray = np.zeros((self.__height*4, self.__width*4))
		file = open(filename, 'wb')
		pickle.dump(self.__width,file)
		pickle.dump(self.__height,file)
		pickle.dump(self.__addressList,file)
		file.close()
		print "Height :", self.__height, " Width :", self.__width
		print "End Of autoAddressing, data saved in", filename
	
	def fileAddressing(self, filename):
		print "fileAddressing..."
		file = open(filename, 'rb')
		self.__width = pickle.load(file)
		self.__height = pickle.load(file)
		self.__addressList = pickle.load(file)
		self.__colorArray = np.zeros((self.__height*4, self.__width*4))
		self.__sensorArray = np.zeros((self.__height*4, self.__width*4))
		file.close()

		print "Height :", self.__height, " Width :", self.__width
		print "End Of fileAddressing, data loaded from", filename


	def __write(self, str):
		self._ser.write(unicode(str))

	def getColorArray(self):
		return self.__colorArray

	def getSensorArray(self):
		return self.__sensorArray