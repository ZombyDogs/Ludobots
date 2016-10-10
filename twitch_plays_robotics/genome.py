import numpy as np
import random
import math
import constants as c
from subprocess import Popen, PIPE
from tree import TREE 
from simulator import SIMULATOR
import pickle

class GENOME:

	def __init__(self,ID):

		self.ID = ID

		self.tree = TREE()

		self.age = 0

		self.Reset()

	def Age(self):

		self.age = self.age + 1

	def Display(self):

		self.Send_To_Simulator(playBlind=False,playPaused=False)

	def Dominates(self,other):

		if ( self.fitness <= other.fitness ):

			if ( self.age <= other.age ):

				if ( (self.fitness == other.fitness) & (self.age==other.age) ):

					i_am_younger = self.ID > other.ID

					return i_am_younger
				else:	
					return True
			else:
				return False
		else:
			return False 

	def Get_Dominated(self):

		return self.dominated

	def Get_Evaluated(self):

		return self.evaluated

	def Get_Fitness(self):

		return self.fitness

	def Get_From_Simulator(self,whatToMaximize):

		self.tree.Evaluate(whatToMaximize)

		self.fitness = self.tree.fitness

		self.evaluated = True

	def More_Fit_Than(self,other):

		return self.fitness > other.fitness

	def Mutate(self):

		self.tree.Mutate()

	def Print(self):

		printString = ''

		printString = printString + '[f: '+str(self.fitness)+'] \t'

                printString = printString + '[a: '+str(self.age)+'] \t'

                printString = printString + '[d: '+str(self.dominated)+'] \t'

                # printString = printString + '[e: '+str(self.evaluated)+'] \t'

		print printString

	def Reset(self):

		self.evaluated = False

		self.fitness = 0.0

		self.dominated = False

	def Save(self):

		self.tree.Save()

	def Send_To_Simulator(self,playBlind,playPaused,evaluationTime):

		self.tree.Send_To_Simulator(playBlind,playPaused,evaluationTime)

	def Set_Dominated(self,dominated):

		self.dominated = dominated

	def Wait_To_Finish(self):

		self.tree.Wait_To_Finish()

