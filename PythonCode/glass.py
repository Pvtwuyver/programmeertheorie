from math import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def sortWidth(list):
	sortedList = sorted(list, key=lambda x: (x[0],x[1]), reverse=True)
	return sortedList
	
def sortHeight(list):
	sortedList = sorted(list, key=lambda x: (x[1],x[0]), reverse=True)
	return sortedList
	
def orientation(list, side):
	if side == "width":
		for item in list:
			bigSide, smallSide = max(item[0],item[1]), min(item[0],item[1])
			item[0], item[1] = bigSide, smallSide
		list = sortWidth(list)
		return list
	elif side == "height":
		for item in list:
			bigSide, smallSide = max(item[0],item[1]), min(item[0],item[1])
			item[0], item[1] = smallSide, bigSide
		list = sortHeight(list)
		return list

def search(list, maxWidth, maxHeight):
	for i in list:
		if (i[0] <= maxWidth) and (i[1] <= maxHeight):
			list.remove(i)
			return i
	return None 
		
def verticalFill(list, W, H, xIndex, yIndex):
	xStart = xIndex
	yStart = yIndex	
	colWidth, rowHeight = W, H
	while len(list) > 0:
		# initial search
		list = orientation(list, "width")
		print("search: ", colWidth, rowHeight, " In list: ", list)
		cut = search(list, colWidth, rowHeight)
		if cut is not None: 
			cutWidth, cutHeight = cut[0], cut[1]
		else:
			# try different orientation
			list = orientation(list, "height")
			cut = search(list, colWidth, rowHeight)
			if cut is not None:
				cutWidth, cutHeight = cut[0], cut[1]
			else:
				# new column needed
				print("new col")
				list = orientation(list, "width")
				xIndex += colWidth
				colWidth = W - (xIndex - xStart)
				yIndex = yStart
				rowHeight = H
				#print("search: ", colWidth, rowHeight)
				cut = search(list, colWidth, rowHeight)
				if cut is not None:
					cutWidth, cutHeight = cut[0], cut[1]
				else:
					list = orientation(list, "height")
					cut = search(list, colWidth, rowHeight)
					if cut is not None: 
						cutWidth, cutHeight = cut[0], cut[1]
					else:
						break
		print("cut: ", cut)
		ax1 = fig1.add_subplot(111, aspect='equal')
		ax1.add_patch(
			patches.Rectangle(
				(xIndex, yIndex),   # (x,y)
				cutWidth,          # width
				cutHeight,          # height
				facecolor = "#efda62"
			)
		)
		if yIndex == yStart:
			colWidth = cutWidth
		# room left?
		
		if (cutHeight > (colWidth - cutWidth)) and ((colWidth - cutWidth) > 0):
			print("list for recursion: ", list)
			list = horizontalFill(list, colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex)
			list = orientation(list, "width")
		elif (cutHeight <= (colWidth - cutWidth)) and ((colWidth - cutWidth) > 0):
			print("list for recursion: ", list)
			list = verticalFill(list, colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex)
		
		yIndex += cutHeight
		rowHeight = H - (yIndex - yStart)
	return list
	
def horizontalFill(list, W, H, xIndex, yIndex):
	xStart = xIndex
	yStart = yIndex	
	colWidth, rowHeight = W, H
	while len(list) > 0:
		print(list)
		# initial search
		list = orientation(list, "height")
		print("search: ", colWidth, rowHeight)
		cut = search(list, colWidth, rowHeight)
		if cut is not None: 
			cutWidth, cutHeight = cut[0], cut[1]
		else:
			# try different orientation
			list = orientation(list, "width")
			cut = search(list, colWidth, rowHeight)
			if cut is not None:
				cutWidth, cutHeight = cut[0], cut[1]
			else:
				# new row needed
				print("new row")
				list = orientation(list, "height")
				yIndex += rowHeight
				rowHeight = H - (yIndex - yStart)
				xIndex = xStart
				colWidth = W
				#print("search: ", colWidth, rowHeight)
				cut = search(list, colWidth, rowHeight)
				if cut is not None:
					cutWidth, cutHeight = cut[0], cut[1]
				else:
					list = orientation(list, "width")
					cut = search(list, colWidth, rowHeight)
					if cut is not None: 
						cutWidth, cutHeight = cut[0], cut[1]
					else:
						break
		print("cut: ", cut)
		ax1 = fig1.add_subplot(111, aspect='equal')
		ax1.add_patch(
			patches.Rectangle(
				(xIndex, yIndex),   # (x,y)
				cutWidth,          # width
				cutHeight,          # height
				facecolor = "#efda62"
			)
		)
		if xIndex == xStart:
			rowHeight = cutHeight
		# room left?
		if (cutWidth > (rowHeight - cutHeight)) and ((rowHeight - cutHeight) > 0):
			list = verticalFill(list, cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight)
			list = orientation(list, "height")
		elif (cutWidth <= (rowHeight - cutHeight)) and ((rowHeight - cutHeight) > 0):
			list = horizontalFill(list, cutWidth, rowHeight - cutHeight, xIndex, yIndex + cutHeight)

		xIndex += cutWidth
		colWidth = W - (xIndex - xStart)
	return list

Width = 600
Height = 500
Area = Width*Height	

order = [[300,100],[250,125],[150,125],[150,180],[130,90],[130,70],[70,50],[100,200],[80,60],[400,400]]

while len(order) > 0:
	fig1 = plt.figure()
	order = verticalFill(order, Width, Height, 0, 0)
	plt.axis([0,Width,0,Height])
	plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
	plt.show()
plt.show