"""""""""""""""""""""
hillclimber.py
Hill climbing

Carglass
"""""""""""""""""""""

from helpers import *
from copy import*

# define window order

""" glasslist 1 """
#glasslist = [[190,270],[90,160],[120,290],[110,220],[160,120],[90,120],[200,100],[110,290],[120,170],[100,320],[90,160],[190,300],[170,250],[180,340],[170,180],[90,100],[110,270],[70,220],[40,130],[140,330],[130,110],[40,240]]

""" glasslist 2,3,4 """
#glasslist = [[150,150],[50,110],[160,270],[130,270],[130,130],[190,160],[200,190],[170,240],[110,220],[110,140],[70,230],[140,170],[160,240],[200,130],[150,100],[190,220],[60,150],[40,240],[110,100],[130,240],[130,220],[90,160],[40,100],[50,140],[150,250],[70,200],[160,120],[120,120],[100,190],[190,240],[120,270],[60,130],[160,230],[170,170],[200,170],[90,210],[60,190],[120,180],[110,190],[180,270],[160,120],[160,100],[90,220],[110,260],[80,120],[80,280],[50,280],[80,270],[160,190],[40,190],[90,250],[180,210],[180,250],[170,270],[140,230],[110,270],[80,140],[100,270],[140,210],[120,200],[120,150]]

""" specified order """
glasslist = [[340, 180], [330, 140], [320, 100], [240, 40], [130, 40], [250, 170], [220, 110], [220, 70], [200, 100], [300, 190], [290, 120], [290, 110], [270, 190], [270, 110], [180, 170], [90, 160], [170, 120], [160, 120], [160, 90], [130, 110], [120, 90], [100, 90]]

""" uncomment for random order """
#glasslist = randomOrder(glasslist)


def main():

	# appoint class
	order1 = Order(list(glasslist))

	# set sheet size
	sheetWidth, sheetHeight = 600, 500

	bestScore = 0
	bestLayout = copy(glasslist)

	scoreList = []

	# number of iterations
	for i in range(100000):
		
		# cut glass
		while len(order1.glasslist) > 0:
			order1.placeVertical("hill", "", sheetWidth, sheetHeight, 0, 0)
			order1.usePerSheet.append(order1.usedGlass)
			order1.numberOfSheets += 1
			order1.usedGlass = 0
		score = order1.score()
		
		# check if score improved
		if score > bestScore:
			bestScore = score
			bestLayout = list(order1.layout)
		print i, bestScore
		scoreList.append(bestScore)

		# reset to best layout and make new swap
		order1.reset(deepcopy(bestLayout))
		if (random.random() < 0.5):
			order1.randomSwap(2)
		else:
			order1.randomTurn()
	
	# plot best sequence of cuts
	bestSeq = Order(bestLayout)
	plotOrder(bestSeq, sheetWidth, sheetHeight)
	
	# show evolution of score
	plotScores(scoreList)
	
	
if __name__ == "__main__":
    main()