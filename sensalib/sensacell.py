#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import util
import serial
import time
import numpy as np
import io
import pickle
from sensalib.util import *

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
		self.__ser = io.TextIOWrapper(io.BufferedRWPair(self.__serUSB,self.__serUSB,1),
							newline = '\r',
							line_buffering = True)
		self.flush(1200)
		self.__colorArray = []
		self.__sensorArray = []
		self.__addressList = {}
		self.__height = 0
		self.__width = 0
		self.__nbModules = 0
		self.__write("0300a00\r")
		self.__previousColorArray = []

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
			line = self.__ser.readline()
			print line
			if len (line) == 9:
				if line[:1]=='0' or line[:1]=='1':
					x=4*(int(line[4:6],16)-1)
					y=4*(int(line[2:4],16)-1)
					if x/4 > self.__width :
						self.__width = x/4 + 1
					if y/4 > self.__height :
						self.__height = y/4 + 1
					self.__addressList[int(line[6:8],16)] = [x,y]
		file = open(filename, 'wb')
		pickle.dump(self.__width,file)
		pickle.dump(self.__height,file)
		pickle.dump(self.__addressList,file)
		self.__arraysInit(self.__height, self.__width)
		file.close()
		print "Height :", self.__height, " Width :", self.__width
		print "End Of autoAddressing, data saved in", filename
	
	def fileAddressing(self, filename):
		print "fileAddressing..."
		file = open(filename, 'rb')
		self.__width = pickle.load(file)
		self.__height = pickle.load(file)
		self.__addressList = pickle.load(file)
		self.__arraysInit(self.__height, self.__width)
		file.close()
		print "Height :", self.__height, " Width :", self.__width
		print "End Of fileAddressing, data loaded from", filename

	def __arraysInit(self, height, width):
		self.__nbModules = width * height
		self.__colorArray = np.zeros((height*4, width*4))
		self.__previousColorArray = np.copy(self.__colorArray)
		self.__sensorArray = np.zeros((height*4, width*4))
		self.__fullDisplay()

	def setColor(self, color, y, x):
		self.__colorArray[y][x] = color

	def moduleDisplay(self, address):
		self.__write("0101a%0.2X\r"%address)
		x = self.__addressList[address][0]
		y = self.__addressList[address][1]
		for i in range(y,y+4):
			for j in range(x,x+4):
				self.__write(util.intToByte(self.__colorArray[i][j]))

	def __fullDisplay(self):
		self.__write("01%0.2Xa01\r"%self.__nbModules)
		for i in range (1, self.__nbModules + 1):
			x = self.__addressList[i][0]
			y = self.__addressList[i][1]
			for i in range(y,y+4):
				for j in range(x,x+4):
					self.__write(util.intToByte(self.__colorArray[i][j]))

	def fullDisplay(self):
		changedModules = []
		for i in range (0,self.__width*4-1):
			for j in range (0,self.__height*4-1):
				if self.__colorArray[j][i] != self.__previousColorArray[j][i]:
					if self.getAddress(j,i) not in changedModules:
						changedModules.append(self.getAddress(j,i))
		if len(changedModules)/self.__nbModules < 0.92:
			for i in changedModules:
				self.moduleDisplay(i)
		else:
			self.__fullDisplay()
		self.__previousColorArray = np.copy(self.__colorArray)
		#return len(changedModules)

	def __write(self, str):
		self.__serUSB.flushInput()
		self.__serUSB.write(str)

	def write(self, str):
		self.__serUSB.write(str)

	def getColorArray(self):
		return self.__colorArray

	def setColorArray(self,array):
		self.__colorArray = array

	def getSensorArray(self):
		return np.copy(self.__sensorArray)

	def getNbModules(self):
		return self.__nbModules

	def getAddress(self,y ,x):
		coord = [x - x%4, y - y%4]
		for key in self.__addressList.keys():
			if coord == self.__addressList[key]:
				return key

	def moduleListenning(self, address):
		self.__write("r%0.2X\r"%address)
		line = self.__ser.readline()
		self.__updateSensorModule(line,address)

	def __updateSensorModule(self, line, address):
		x = self.__addressList[address][0]
		y = self.__addressList[address][1]
		binaryLine =  "{0:1b}".format(int(line,16),"0").zfill(16)
		k = 0
		for i in range(y,y+4):
			for j in range(x,x+4):
				self.__sensorArray[i][j] = int(binaryLine[k])*(0xFF0000)
				k+=1

	def fullListenning(self):
		self.__write("00%0.2Xa01\r"%self.__nbModules)
		line = self.__ser.readline()
		for i in range(1,self.__nbModules+1):
			self.__updateSensorModule(line[(i-1)*4:((i-1)*4)+4],i)

	def flush(self, nbBytesToflush):
		for i in range(1,nbBytesToflush):
			self.__write("\r")