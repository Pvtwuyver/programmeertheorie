from math import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def totalArea(list):
	area = 0
	for i in list:
		area += i[0]*i[1]
	return area

def sortWidth(list):
	sortedList = sorted(list, key=lambda x: (x[0],x[1]), reverse=True)
	return sortedList
	
def sortHeight(list):
	sortedList = sorted(list, key=lambda x: (x[1],x[0]), reverse=True)
	return sortedList
	
def sortArea(list):
	sortedList = sorted(list, key=lambda x: (x[1]*x[0]), reverse=True)
	return sortedList
	
def sortCirc(list):
	sortedList = sorted(list, key=lambda x: (x[1]+x[0]), reverse=True)
	return sortedList
	
def orientation(list, side):
	if side == "width":
		for item in list:
			bigSide, smallSide = max(item[0],item[1]), min(item[0],item[1])
			item[0], item[1] = bigSide, smallSide
		#list = sortCirc(list)
		list = sortWidth(list)
		return list
	elif side == "height":
		for item in list:
			bigSide, smallSide = max(item[0],item[1]), min(item[0],item[1])
			item[0], item[1] = smallSide, bigSide
		#list = sortCirc(list)
		list = sortHeight(list)
		return list

def search(list, maxWidth, maxHeight, type):
	while type > 0:
		for i in list:
			if (i[0] <= maxWidth) and (i[1] <= maxHeight) and (i[2] == type):
				list.remove(i)
				return i
		type -= 1
	return None
	
def verticalFill(list, W, H, xIndex, yIndex, type):
	xStart = xIndex
	yStart = yIndex	
	colWidth, rowHeight = W, H
	while len(list) > 0:
		# initial search
		list = orientation(list, "width")
		cut = search(list, colWidth, rowHeight, type)
		if cut is not None: 
			cutWidth, cutHeight, cutType = cut[0], cut[1], cut[2]
		else:
			# try different orientation
			list = orientation(list, "height")
			cut = search(list, colWidth, rowHeight, type)
			if cut is not None:
				cutWidth, cutHeight, cutType = cut[0], cut[1], cut[2]
			else:
				# new column needed
				list = orientation(list, "width")
				xIndex += colWidth
				colWidth = W - (xIndex - xStart)
				yIndex = yStart
				rowHeight = H
				#print("search: ", colWidth, rowHeight)
				cut = search(list, colWidth, rowHeight, type)
				if cut is not None:
					cutWidth, cutHeight, cutType = cut[0], cut[1], cut[2]
				else:
					list = orientation(list, "height")
					cut = search(list, colWidth, rowHeight, type)
					if cut is not None: 
						cutWidth, cutHeight, cutType = cut[0], cut[1], cut[2]
					else:
						break
		ax1 = fig1.add_subplot(111, aspect='equal')
		ax1.add_patch(
			patches.Rectangle(
				(xIndex, yIndex),   # (x,y)
				cutWidth,          # width
				cutHeight,          # height
				facecolor = cutColor(cutType)
			)
		)
		if yIndex == yStart:
			colWidth = cutWidth
		# room left?
		
		if (cutHeight > (colWidth - cutWidth)) and ((colWidth - cutWidth) > 0):
			list = horizontalFill(list, colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex, type)
			list = orientation(list, "width")
		elif (cutHeight <= (colWidth - cutWidth)) and ((colWidth - cutWidth) > 0):
			list = verticalFill(list, colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex, type)
		
		yIndex += cutHeight
		rowHeight = H - (yIndex - yStart)
	return list
	
def horizontalFill(list, W, H, xIndex, yIndex, type):
	xStart = xIndex
	yStart = yIndex	
	colWidth, rowHeight = W, H
	while len(list) > 0:
		# initial search
		list = orientation(list, "height")
		cut = search(list, colWidth, rowHeight, type)
		if cut is not None: 
			cutWidth, cutHeight, cutType = cut[0], cut[1], cut[2]
		else:
			# try different orientation
			list = orientation(list, "width")
			cut = search(list, colWidth, rowHeight, type)
			if cut is not None:
				cutWidth, cutHeight, cutType = cut[0], cut[1], cut[2]
			else:
				# new row needed
				list = orientation(list, "height")
				yIndex += rowHeight
				rowHeight = H - (yIndex - yStart)
				xIndex = xStart
				colWidth = W
				#print("search: ", colWidth, rowHeight)
				cut = search(list, colWidth, rowHeight, type)
				if cut is not None:
					cutWidth, cutHeight, cutType = cut[0], cut[1], cut[2]
				else:
					list = orientation(list, "width")
					cut = search(list, colWidth, rowHeight, type)
					if cut is not None: 
						cutWidth, cutHeight, cutType = cut[0], cut[1], cut[2]
					else:
						break
		ax1 = fig1.add_subplot(111, aspect='equal')
		ax1.add_patch(
			patches.Rectangle(
				(xIndex, yIndex),   # (x,y)
				cutWidth,          # width
				cutHeight,          # height
				facecolor = cutColor(cutType)
			)
		)
		if xIndex == xStart:
			rowHeight = cutHeight
		# room left?
		if (cutWidth > (rowHeight - cutHeight)) and ((rowHeight - cutHeight) > 0):
			list = verticalFill(list, cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight, type)
			list = orientation(list, "height")
		elif (cutWidth <= (rowHeight - cutHeight)) and ((rowHeight - cutHeight) > 0):
			list = horizontalFill(list, cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight, type)

		xIndex += cutWidth
		colWidth = W - (xIndex - xStart)
	return list

def cutColor(type):
	if type == 1:
		color = "#efda62"
	elif type == 2:
		color = "#616bef"
	elif type == 3:
		color = "#ef6161"
	return color

# glaslijst 5:
order = [[130,240,1],
[170,190,1],
[150,150,1],
[70,160,1],
[160,210,1],
[110,140,1],
[110,170,1],
[150,170,1],
[150,230,1],
[60,120,1],
[160,150,1],
[160,240,1],
[70,160,1],
[120,230,1],
[140,120,1],
[130,240,1],
[90,180,1],
[150,230,1],
[100,150,1],
[80,180,1],
[130,180,1],
[150,210,2],
[150,150,2],
[100,230,2],
[110,110,2],
[70,240,2],
[150,230,2],
[170,220,2],
[150,190,2],
[180,210,2],
[130,120,2],
[170,230,2],
[90,200,2],
[150,230,2],
[140,190,2],
[120,130,2],
[160,150,2],
[110,100,2],
[80,190,2],
[80,230,2],
[70,180,2],
[180,100,3],
[90,130,3],
[70,180,3],
[150,120,3],
[60,200,3],
[80,200,3],
[60,240,3],
[110,160,3],
[120,240,3],
[110,170,3],
[150,230,3]]

beginArea = totalArea(order)
wasteArray = []
numberOfSheets = 0

# type 3
Width = 400
Height = 400
Area = Width*Height	

while [i[2] for i in order].count(3) > 0:

	fig1 = plt.figure()
	order = verticalFill(order, Width, Height, 0, 0, 3)
	waste = Area - (beginArea - totalArea(order))
	beginArea = beginArea - (beginArea - totalArea(order))
	wasteArray.append(waste)
	plt.axis([0,Width,0,Height])
	plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
	plt.title('Type 3 glas (4x4)')
	plt.plot()
	numberOfSheets += 1

# type 2
Width = 500
Height = 400
Area = Width*Height	

while [i[2] for i in order].count(2) > 0:

	fig1 = plt.figure()
	order = verticalFill(order, Width, Height, 0, 0, 3)
	waste = Area - (beginArea - totalArea(order))
	beginArea = beginArea - (beginArea - totalArea(order))
	wasteArray.append(waste)
	plt.axis([0,Width,0,Height])
	plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
	plt.title('Type 2 glas (5x4)')
	plt.plot()
	numberOfSheets += 1

# type 3
Width = 600
Height = 500
Area = Width*Height	

while [i[2] for i in order].count(1) > 0:

	fig1 = plt.figure()
	order = verticalFill(order, Width, Height, 0, 0, 3)
	waste = Area - (beginArea - totalArea(order))
	beginArea = beginArea - (beginArea - totalArea(order))
	wasteArray.append(waste)
	plt.axis([0,Width,0,Height])
	plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
	plt.title('Type 1 glas (6x5)')
	plt.plot()
	numberOfSheets += 1



plt.show()

score = (Area - (sum(wasteArray[0:-1])/numberOfSheets))/float(Area)

print("Score: ", score)
