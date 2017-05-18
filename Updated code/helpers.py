"""""""""""""""""""""
helpers.py
Contains helper functions and classes

Carglass
"""""""""""""""""""""

from math import *
from copy import *
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Order:
	
	def __init__(self, glasslist):
	
		self.glasslist = glasslist # list of windows
		self.startlist = list(glasslist) # remember starting point (copy)
		self.orderArea = totalArea(glasslist)
		self.layout = [] # order in which windows are cut
		self.usedGlass = 0
		self.numberOfSheets = 0
	
	def sortWidth(self):
		# sort by width
		self.glasslist = sorted(self.glasslist, key=lambda x: (x[0],x[1]), reverse=True)
		
	def sortHeight(self):
		# sort by height
		self.glasslist = sorted(self.glasslist, key=lambda x: (x[1],x[0]), reverse=True)
	
	def sortArea(self):
		# sort by area
		self.glasslist = sorted(self.glasslist, key=lambda x: (x[1]*x[0]), reverse=True)
		
	def sortCirc(self):
		# sort by circumference
		self.glasslist = sorted(self.glasslist, key=lambda x: (x[1]+x[0]), reverse=True)
	
	def score(self):
		temp  = float((self.orderArea/(600*500)))/self.numberOfSheets
		score = (self.orderArea/float(self.usedGlass))*temp
		return score, self.numberOfSheets
		
	def reset(self, inputList):
		self.glasslist = copy(inputList)
		self.layout = []
		self.usedGlass = 0
		self.numberOfSheets = 0
		
	def randomSwap(self, numberOfSwaps):
		for i in range(numberOfSwaps):
			# pick random windows
			n = random.randint(0, len(self.glasslist)-1)
			m = random.randint(0, len(self.glasslist)-1)
			# make sure windows have same orientation
			if self.glasslist[n][0] > self.glasslist[n][1]:
				self.glasslist[m][0], self.glasslist[m][1] = max(self.glasslist[m]), min(self.glasslist[m])
			elif self.glasslist[n][0] < self.glasslist[n][1]:
				self.glasslist[m][0], self.glasslist[m][1] = min(self.glasslist[m]), max(self.glasslist[m])
			# swap items
			self.glasslist[n], self.glasslist[m] = self.glasslist[m], self.glasslist[n]
		
	def search(self, maxWidth, maxHeight, method):
		# select a window from glasslist
	
		if method == "greedy":
			# search for largest fitting window
			for i in self.glasslist:
				if (i[0] <= maxWidth) and (i[1] <= maxHeight):
					self.glasslist.remove(i)
					return i
			# try different orientation
			for i in self.glasslist:
				if (i[1] <= maxWidth) and (i[0] <= maxHeight):
					self.glasslist.remove(i)
					return i[::-1]
			
			# nothing found, return "None"
			return None	

		elif method == "random":
			cut = [0,0]
			counter = 0
			while len(self.glasslist) > 0:
				# randomize window
				temp = random.choice(self.glasslist)
				# randomize orientation
				if (random.random() < 0.5):
					cut = temp[::-1]
				else:
					cut = temp
				# check if it fits
				if (cut[0] <= maxWidth) and (cut[1] <= maxHeight):
					self.glasslist.remove(temp)
					return cut
				# count number of search iterations
				counter += 1
				if counter > 1000:
					# stop searching after 1000 iterations
					return None
		else:
			cut = self.glasslist[0]
			if (cut[0] <= maxWidth) and (cut[1] <= maxHeight):
				self.glasslist.remove(cut)
				return cut
			return None
	
	
	def changeOrientation(self, side):
	
		# change orientation of windows
		if side == "width":
			# maximize width
			for item in self.glasslist:
				bigSide, smallSide = max(item[0],item[1]), min(item[0],item[1])
				item[0], item[1] = bigSide, smallSide
			self.sortWidth()
			#self.sortArea()
		elif side == "height":
			# maximize height
			for item in self.glasslist:
				bigSide, smallSide = max(item[0],item[1]), min(item[0],item[1])
				item[0], item[1] = smallSide, bigSide
			self.sortHeight()		
			#self.sortArea()
		
	def placeVertical(self, method, figure, sheetWidth, sheetHeight, xIndex, yIndex):
	
		# cut windows using greedy principle (vertically)
		xStart = xIndex
		yStart = yIndex	
		colWidth, rowHeight = sheetWidth, sheetHeight # cutting bounds
		
		while len(self.glasslist) > 0:	
		
			self.changeOrientation("width") if method == "greedy" else False
			# search for best fitting window
			cut = self.search(colWidth, rowHeight, method)
			if cut is not None: 
				cutWidth, cutHeight = cut[0], cut[1]
			else:
				# start new column
				xIndex += colWidth
				colWidth = sheetWidth - (xIndex - xStart)
				yIndex = yStart
				rowHeight = sheetHeight
				# now search for best window
				cut = self.search(colWidth, rowHeight, method)
				if cut is not None: 
					cutWidth, cutHeight = cut[0], cut[1]
				else:		
					# no fitting window left
					break
			# draw rectangle and add to memory
			addRectangle(figure, xIndex, yIndex, cutWidth, cutHeight) if (method != "random") and (method != "hill") else False		
			self.layout.append(cut)	
			if yIndex == yStart:
				# set column width if first cut
				colWidth = cutWidth
				if yIndex == 0:
					# add column to used glass
					self.usedGlass += cutWidth*sheetHeight
			# room left?	
			if (cutHeight > (colWidth - cutWidth)) and ((colWidth - cutWidth) > 0) and (method == "greedy"):
				self.placeHorizontal(method, figure, colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex)
				self.changeOrientation("width") if method == "greedy" else False
			else:#elif (cutHeight <= (colWidth - cutWidth)) and ((colWidth - cutWidth) > 0):
				self.placeVertical(method, figure, colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex)
			# update (x,y)		
			yIndex += cutHeight
			rowHeight = sheetHeight - (yIndex - yStart)				
			
	def placeHorizontal(self, method, figure, sheetWidth, sheetHeight, xIndex, yIndex):
	
		# cut windows using greedy principle (horizontally)
		xStart = xIndex
		yStart = yIndex	
		colWidth, rowHeight = sheetWidth, sheetHeight # cutting bounds
		
		while len(self.glasslist) > 0:	
		
			self.changeOrientation("height") if method == "greedy" else False
			# search for best fitting window
			cut = self.search(colWidth, rowHeight, method)
			if cut is not None: 
				cutWidth, cutHeight = cut[0], cut[1]
			else:
				# start new row
				yIndex += rowHeight
				rowHeight = sheetHeight - (yIndex - yStart)
				xIndex = xStart
				colWidth = sheetWidth
				# now search for best window
				cut = self.search(colWidth, rowHeight, method)
				if cut is not None: 
					cutWidth, cutHeight = cut[0], cut[1]
				else:		
					# no fitting window left
					break
			# draw rectangle and add to memory
			addRectangle(figure, xIndex, yIndex, cutWidth, cutHeight) if (method != "random") and (method != "hill") else False		
			self.layout.append(cut)	
			if xIndex == xStart:
				# set row height if first cut
				rowHeight = cutHeight
				if xIndex == 0:
					# add column to used glass
					self.usedGlass += cutHeight*sheetWidth
			# room left?
			"""
			if (cutWidth > (rowHeight - cutHeight)) and ((rowHeight - cutHeight) > 0):
				# fill vertical if width>height
				self.placeVertical(method, figure, cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight)
				self.changeOrientation("height") if method == "greedy" else False
			"""
			if (cutWidth <= (rowHeight - cutHeight)) and ((rowHeight - cutHeight) > 0) and (method == "greedy"):
				# fill horizontal if height>width
				self.placeHorizontal(method, figure, cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight)
			else:
				# fill vertical if width>height
				self.placeVertical(method, figure, cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight)
				self.changeOrientation("height") if method == "greedy" else False
			# update (x,y)		
			xIndex += cutWidth
			colWidth = sheetWidth - (xIndex - xStart)
					

		
		
def totalArea(list):
	area = 0
	for i in list:
		area += i[0]*i[1]
	return area					
					
					
def addRectangle(figure, xIndex, yIndex, cutWidth, cutHeight):
	ax1 = figure.add_subplot(111, aspect='equal')
	ax1.add_patch(
		patches.Rectangle(
			(xIndex, yIndex),   # (x,y)
			cutWidth,          # width
			cutHeight,          # height
			facecolor = "#efda62"
		)
	)

