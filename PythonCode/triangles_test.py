from math import *
import operator
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def sortTri(list):
	sortedList = sorted(list, reverse=True)
	return sortedList
	
def calcAngles(f):
	alpha = acos((f[0]**2 + f[2]**2 - f[1]**2)/(2.0 * f[2] * f[0]))
	beta = acos((f[0]**2 + f[1]**2 - f[2]**2)/(2.0 * f[1] * f[0]))
	gamma = acos((f[2]**2 + f[1]**2 - f[0]**2)/(2.0 * f[2] * f[1]))
	return alpha, beta, gamma
	
def searchHeight(classList, maxWidth, maxHeight):
	classList.sort(key=lambda x: (x.height, x.sides[0], x.sides[1], x.sides[2]), reverse=True)
	for i in classList:
		if (i.height <= maxHeight) and (i.sides[0] <= maxWidth):
			classList.remove(i)
			return i
	return None 
	
def searchTriangle(classList, side1, side2, side3):
	classList.sort(key=lambda x: (x.height, x.sides[0], x.sides[1], x.sides[2]), reverse=True)
	for i in classList:
		if (i.sides[0] <= side1) and (i.sides[1] <= side2) and (i.sides[2] <= side3):
			classList.remove(i)
			return i
	return None 
	

def distance(point1,point2):
	d = sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
	return d



class Triangle:
	
	def __init__(self, sides):
		self.sides = sortTri(sides)
		self.angles = calcAngles(self.sides)
		self.height = sides[1]*sin(self.angles[1])
	
	

order = [
  [130,100,205],
  [160,180,327],
  [100,160,211],
  [120,200,302],
  [120,180,286],
  [190,180,360],
  [190,170,343],
  [130,140,260],
  [160,200,343],
  [140,180,303],
  [200,190,380],
  [110,190,178],
  [100,200,284],
  [160,150,300],
  [120,130,240],
  [170,180,340],
  [170,130,278],
  [110,130,223],
  [130,150,261],
  [110,120,220],
  [180,110,220],
  [110,140,238],
  [150,110,234],
  [170,180,340],
  [160,200,343],
  [120,150,251],
  [160,170,320],
  [200,160,339],
  [180,170,340],
  [170,110,250],
  [140,110,220],
  [120,140,244],
  [140,180,305],
  [150,190,321],
  [150,160,300],
  [160,130,262],
  [130,170,278],
  [130,140,260],
  [110,190,178],
  [110,110,110],
  [200,130,266],
  [110,100,170]
]

classes = []
for i in order:
	classes.append(Triangle(i))
	
#classes.sort(key=operator.attrgetter('height'), reverse=True)
classes.sort(key=lambda x: (x.height, x.sides[0], x.sides[1], x.sides[2]), reverse=True)


Width = 600
Height = 500
Area = Width*Height	

xIndex = 0
yIndex = 0


def triangleFill(classList, W, H, xIndex, yIndex):
	xStart = xIndex
	yStart = yIndex	
	colWidth, rowHeight = W, H
	while len(classList) > 0:
		# initial search
		cut = searchHeight(classList, colWidth, rowHeight)
		if cut is None:
			# new row
			yIndex += rowHeight
			rowHeight = H - (yIndex - yStart)
			xIndex = xStart
			colWidth = W
			cut = searchHeight(classList, colWidth, rowHeight)
			if cut is None:
				break;
		ax1 = fig1.add_subplot(111, aspect='equal')
		ax1.add_patch(
			patches.Polygon(
				[[xIndex,yIndex],[xIndex+cut.sides[0],yIndex],[xIndex+cut.sides[0]-(cut.sides[1]*cos(cut.angles[1])),yIndex+cut.height]],
				closed = True,
				linewidth=1,
				facecolor = "#efda62"
			)
		)
		if xStart == xIndex:
			rowHeight = cut.height
			corner1 = 0
		
		corner2 = [xIndex,yIndex]
		corner3 = [xIndex+cut.sides[0]-(cut.sides[1]*cos(cut.angles[1])),yIndex+rowHeight]

		if ('corner1' in locals()) and (corner1 != 0):
			cut2 = searchTriangle(classList, distance(corner1,corner3), distance(corner1,corner2), distance(corner2,corner3))			
			if cut2 is not None:	
				beta2 = calcAngles([distance(corner1,corner3), distance(corner1,corner2), distance(corner2,corner3)])
				print(cut2.angles[1], beta2[0])
				if cut2.angles[1] > beta2[0]:
					#print("True")
					corners = [[corner1[0]+cut2.sides[0], yIndex + rowHeight],corner1,[corner1[0]+(cut2.sides[1]*cos(cut2.angles[1])),yIndex + rowHeight-cut2.height]]
					#corners = [corner3,[corner3[0]-cut2.sides[0],yIndex + rowHeight],[corner3[0]-cut2.sides[0]+(cut2.sides[1]*cos(cut2.angles[1])),yIndex + rowHeight-cut2.height]]
				else:
					#print("---")
					corners = [corner3,[corner3[0]-cut2.sides[0],yIndex + rowHeight],[corner3[0]-cut2.sides[0]+(cut2.sides[1]*cos(cut2.angles[1])),yIndex + rowHeight-cut2.height]]
				#print(cut2.angles[1], beta2[1])
				ax1 = fig1.add_subplot(111, aspect='equal')
				ax1.add_patch(
					patches.Polygon(
						#[corner3,[corner3[0]-cut2.sides[0],yIndex + rowHeight],[corner3[0]-cut2.sides[0]+(cut2.sides[1]*cos(cut2.angles[1])),yIndex + rowHeight-cut2.height]],
						corners,
						closed = True,
						linewidth=1,
						facecolor = "#efda62"
					)
				)				
				#print [corner3,[corner3[0]-cut2.sides[0],rowHeight],[corner3[0]-cut2.sides[0]+(cut2.sides[1]*cos(cut2.angles[1])),rowHeight-cut2.height]]
		xIndex += cut.sides[0]
		colWidth = W - (xIndex - xStart)
		corner1 = corner3
	return classList


	
while len(classes) > 0:
	fig1 = plt.figure()
	classes = triangleFill(classes, Width, Height, 0, 0)
	plt.axis([0,Width,0,Height])
	plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
	plt.plot()

plt.show()
