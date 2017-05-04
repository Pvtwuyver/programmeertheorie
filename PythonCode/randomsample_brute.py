from math import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import numpy as np
		
def verticalFill(list, W, H, xIndex, yIndex, layout):
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
		layout.append([xIndex, yIndex, cutWidth, cutHeight])
		if yIndex == yStart:
			colWidth = cutWidth
		# room left?
		list, layout = verticalFill(list, colWidth - cutWidth, cutHeight, xIndex + cutWidth, yIndex, layout)	
		yIndex += cutHeight
		rowHeight = H - (yIndex - yStart)
	return list, layout
	
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

# glaslijst 1
order = [[190,270],[90,160],[120,290],[110,220],[160,120],[90,120],[200,100],[110,290],[120,170],[100,320],[90,160],[190,300],[170,250],[180,340],[170,180],[90,100],[110,270],[70,220],[40,130],[140,330],[130,110],[40,240]]
# glaslijst 2
#order = [[150,150],[50,110],[160,270],[130,270],[130,130],[190,160],[200,190],[170,240],[110,220],[110,140],[70,230],[140,170],[160,240],[200,130],[150,100],[190,220],[60,150],[40,240]]
# glaslijst 3:
#order = [[110,100],[130,240],[130,220],[90,160],[40,100],[50,140],[150,250],[70,200],[160,120],[120,120],[100,190],[190,240],[120,270],[60,130],[160,230],[170,170],[200,170],[90,210],[60,190],[120,180],[110,190],[180,270],[160,120],[160,100]]
# glaslijst 4:
#order = [[90,220],[110,260],[80,120],[80,280],[50,280],[80,270],[160,190],[40,190],[90,250],[180,210],[180,250],[170,270],[140,230],[110,270],[80,140],[100,270],[140,210],[120,200],[120,150]]
# glaslijst 2,3 en 4
#order = [[150,150],[50,110],[160,270],[130,270],[130,130],[190,160],[200,190],[170,240],[110,220],[110,140],[70,230],[140,170],[160,240],[200,130],[150,100],[190,220],[60,150],[40,240],[110,100],[130,240],[130,220],[90,160],[40,100],[50,140],[150,250],[70,200],[160,120],[120,120],[100,190],[190,240],[120,270],[60,130],[160,230],[170,170],[200,170],[90,210],[60,190],[120,180],[110,190],[180,270],[160,120],[160,100],[90,220],[110,260],[80,120],[80,280],[50,280],[80,270],[160,190],[40,190],[90,250],[180,210],[180,250],[170,270],[140,230],[110,270],[80,140],[100,270],[140,210],[120,200],[120,150]]
beginOrder = list(order)
print(len(beginOrder))

def totalArea(list):
	area = 0
	for i in list:
		area += i[0]*i[1]
	return area

sheets = []
scores = []
best = 0
bestLayout = []

for i in range(0,10000):
	beginArea = totalArea(order)
	wasteArray = []
	locations = []
	totalLayout = []
	numberOfSheets = 0
	
	while len(order) > 0:
		order, sheetLayout = verticalFill(order, Width, Height, 0, 0, [])
		waste = Area - (beginArea - totalArea(order))
		beginArea = beginArea - (beginArea - totalArea(order))
		wasteArray.append(waste)
		totalLayout.append(sheetLayout)
		numberOfSheets += 1
	
	score = (Area - (sum(wasteArray[0:-1])/numberOfSheets))/float(Area)
	if score > best:
		best = score
		bestLayout = list(totalLayout)
	scores.append(best)
	print(i,best)
	order = list(beginOrder)

cutOrder = []	

for s in bestLayout:
	fig1 = plt.figure()
	for w in s:
		ax1 = fig1.add_subplot(111, aspect='equal')
		ax1.add_patch(
			patches.Rectangle(
				(w[0], w[1]),   # (x,y)
				w[2],          # width
				w[3],          # height
				facecolor = "#efda62"
			)
		)
		cutOrder.append([w[2],w[3]])
	plt.axis([0,Width,0,Height])
	plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
	plt.plot()

plt.show()
fig2 = plt.figure()
plt.axis([0,len(scores),0.80,1])
line1 = plt.plot(scores, label="random", linewidth=2)
line2 = plt.plot((0,len(scores)),(0.924,0.924),"k--", linewidth=2)
plt.show()
print(cutOrder)