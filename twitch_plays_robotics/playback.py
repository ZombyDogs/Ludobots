from tree import TREE
import os
import pickle
import sys
import constants as c

whatToMaximize = sys.argv[1]

while 1:

	if ( os.path.exists('best.txt') ):
	
        	f = open('best.txt','rb')
        	parent = pickle.load(f)
        	f.close()

		parent.Send_To_Simulator(playPaused = False, playBlind = False, evaluationTime = c.evaluationTime)

		parent.Evaluate(whatToMaximize)

		print parent.fitness

