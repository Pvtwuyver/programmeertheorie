"""""""""""""""""""""
randomsampling.py
Cut glass randomly

Carglass
"""""""""""""""""""""

from helpers import *

# define window order

""" glasslist 1 """
glasslist = [[190,270],[90,160],[120,290],[110,220],[160,120],[90,120],[200,100],[110,290],[120,170],[100,320],[90,160],[190,300],[170,250],[180,340],[170,180],[90,100],[110,270],[70,220],[40,130],[140,330],[130,110],[40,240]]

""" glasslist 2,3,4 """
#glasslist = [[150,150],[50,110],[160,270],[130,270],[130,130],[190,160],[200,190],[170,240],[110,220],[110,140],[70,230],[140,170],[160,240],[200,130],[150,100],[190,220],[60,150],[40,240],[110,100],[130,240],[130,220],[90,160],[40,100],[50,140],[150,250],[70,200],[160,120],[120,120],[100,190],[190,240],[120,270],[60,130],[160,230],[170,170],[200,170],[90,210],[60,190],[120,180],[110,190],[180,270],[160,120],[160,100],[90,220],[110,260],[80,120],[80,280],[50,280],[80,270],[160,190],[40,190],[90,250],[180,210],[180,250],[170,270],[140,230],[110,270],[80,140],[100,270],[140,210],[120,200],[120,150]]

def main():

	# appoint class
	order1 = Order(list(glasslist))

	# set sheet size
	sheetWidth, sheetHeight = 600, 500

	bestScore = 0
	bestLayout = []
	scoreList = []

	# number of random samples
	for i in range(0,1):
		
		# cut glass
		while len(order1.glasslist) > 0:
			order1.placeVertical("random", "", sheetWidth, sheetHeight, 0, 0)
			order1.usePerSheet.append(order1.usedGlass)
			order1.numberOfSheets += 1
			order1.usedGlass = 0
		score = order1.score()

		# check if score improved
		if score > bestScore:
			bestScore = score
			bestLayout = order1.layout
		print i, bestScore
		scoreList.append(bestScore)
		
		# reset glasslist
		order1.reset(list(glasslist))

	# show best sequence of cuts
	bestSeq = Order(bestLayout)
	plotOrder(bestSeq, sheetWidth, sheetHeight)
	
	# show evolution of score
	plotScores(scoreList)

	
if __name__ == "__main__":
    main()