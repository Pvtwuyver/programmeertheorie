from math import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import numpy as np
	
		
def verticalFill(list, W, H, xIndex, yIndex):
	xStart = xIndex
	yStart = yIndex	
	colWidth, rowHeight = W, H
	while len(list) > 0:
		# initial search
		cut = randomCut(list, colWidth, rowHeight)
		if cut is not None: 
			cutWidth, cutHeight = cut[0], cut[1]
		else:
			# new column needed
			xIndex += colWidth
			colWidth = W - (xIndex - xStart)
			yIndex = yStart
			rowHeight = H
			cut = randomCut(list, colWidth, rowHeight)
			if cut is not None:
				cutWidth, cutHeight = cut[0], cut[1]
			else:
				break
		if yIndex == yStart:
			colWidth = cutWidth
		# room left?
		list = verticalFill(list, colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex)	
		yIndex += cutHeight
		rowHeight = H - (yIndex - yStart)
	return list
	
def randomCut(list, maxWidth, maxHeight):
	cut = [0,0]
	counter = 0
	while (counter < 1000) and len(list) > 0:
		temp = random.choice(list)
		if (random.random() < 0.5):
			cut = temp[::-1]
		else:
			cut = temp
		if (cut[0] <= maxWidth) and (cut[1] <= maxHeight):
			list.remove(temp)
			return cut
		counter += 1
		if counter > 1000:
			return None



Width = 600
Height = 500
Area = Width*Height	

order = [
[190,270],
[90,160],
[120,290],
[110,220],
[160,120],
[90,120],
[200,100],
[110,290],
[120,170],
[100,320],
[90,160],
[190,300],
[170,250],
[180,340],
[170,180],
[90,100],
[110,270],
[70,220],
[40,130],
[140,330],
[130,110],
[40,240]]
beginOrder = list(order)

def totalArea(list):
	area = 0
	for i in list:
		area += i[0]*i[1]
	return area

	
scores = []
best = 1000000
for i in range(0,300):
	beginArea = totalArea(order)
	wasteArray = []
	numberOfSheets = 0
	
	while len(order) > 0:

		order = verticalFill(order, Width, Height, 0, 0)
		waste = Area - (beginArea - totalArea(order))
		beginArea = beginArea - (beginArea - totalArea(order))
		wasteArray.append(waste)

		numberOfSheets += 1
	
	score = sum(wasteArray[0:-1])/numberOfSheets
	if score < best:
		best = score
	scores.append(best)
	print(best)
	order = list(beginOrder)
	
print(scores)