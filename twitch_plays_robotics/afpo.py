from genome import GENOME
import constants
import copy
import random
import numpy as np
import copy
import sys

class AFPO:

	def __init__(self,whatToMaximize):

                # random.seed(0)

                # np.random.seed(0)

		self.whatToMaximize = whatToMaximize

		self.genomes = {}

		self.nextAvailableID = 0

		for g in range(0,constants.popSize):

			self.genomes[g] = GENOME(self.nextAvailableID)

			self.nextAvailableID = self.nextAvailableID + 1

        def Advance_One_Generation(self):

                self.Find_Pareto_Front()

                self.Sort_By_Dominated()

                self.Count_NonDominated_Solutions()

		self.Sort_NonDominated_By_Fitness()

		# self.Save_Best()

		self.Save_Random_Robot_From_Pareto_Front()

		# self.Display_Best()

                self.Delete_Dominated_Solutions()

                self.Print()

                self.Age_NonDominated_Solutions()

                self.Fill()

                self.Evaluate_All()

	def Age_NonDominated_Solutions(self):

		for g in range(0,constants.popSize):

			if ( g in self.genomes ):

				self.genomes[g].Age()

	def Count_NonDominated_Solutions(self):

		self.numNonDominated = 0

		for g in range(0,constants.popSize):

			if ( self.genomes[g].Get_Dominated() == False ):

				self.numNonDominated = self.numNonDominated + 1

	def Delete_Dominated_Solutions(self):

		for g in range(self.numNonDominated,constants.popSize):

			del self.genomes[g]

	def Display_Best(self):

		self.genomes[0].Display()

	def Evaluate_All(self):

		self.genomes[0].evaluated = False

		for g in range(0,constants.popSize):

			if ( self.genomes[g].Get_Evaluated() == False ):

                                self.genomes[g].Send_To_Simulator(playBlind=True,playPaused=False,evaluationTime=constants.evaluationTime)

		for g in range(0,constants.popSize):

                        if ( self.genomes[g].Get_Evaluated() == False ):

                                self.genomes[g].Get_From_Simulator(self.whatToMaximize)

        def Evolve(self):

                self.Evaluate_All()

		for g in range(0,constants.numGenerations):

			print g,constants.numGenerations

			self.Advance_One_Generation()

	def Fill(self):

		self.Spawn_Mutants_From_Pareto_Front()

		self.Inject_New_Genome()

	def Find_Pareto_Front(self):

		self.Make_All_Genomes_NonDominated()

		for i in range(0,constants.popSize):

			for j in range(0,constants.popSize):

				if ( i != j ):

					j_dominates_i = self.genomes[j].Dominates( self.genomes[i] )

					if ( j_dominates_i ):

						self.genomes[i].Set_Dominated( True )

	def Inject_New_Genome(self):

		self.genomes[constants.popSize-1] = GENOME(self.nextAvailableID)

		self.nextAvailableID = self.nextAvailableID + 1

	def Make_All_Genomes_NonDominated(self):

		for g in range(0,constants.popSize):

			self.genomes[g].Set_Dominated(False)

	def Print(self):

		for g in range(0,constants.popSize):

			if ( g in self.genomes ):

				self.genomes[g].Print()		

		print ''

	def Save_Best(self):

		self.genomes[0].Save()

	def Save_Random_Robot_From_Pareto_Front(self):

		selectedGenome = random.randint(0,self.numNonDominated-1)

		self.genomes[selectedGenome].Save()

		
	def Sort_By_Dominated(self):

		length = len(self.genomes) - 1

		sorted = False

		while not sorted:

			sorted = True

			for i in range(length):

				if ( (self.genomes[i].Get_Dominated()==True) and (self.genomes[i+1].Get_Dominated()==False) ):

					sorted = False

					self.genomes[i], self.genomes[i+1] = self.genomes[i+1], self.genomes[i]

        def Sort_NonDominated_By_Fitness(self):

                length = self.numNonDominated - 1

                sorted = False

                while not sorted:

                        sorted = True

                        for i in range(length):

                                if ( self.genomes[i].Get_Fitness() > self.genomes[i+1].Get_Fitness() ):

                                        sorted = False

                                        self.genomes[i], self.genomes[i+1] = self.genomes[i+1], self.genomes[i]


        def Spawn_Mutants_From_Pareto_Front(self):

                for g in range(self.numNonDominated,constants.popSize-1):

                        genomeIndexToCopy = random.randint(0,self.numNonDominated-1)

                        self.genomes[g] = copy.deepcopy( self.genomes[genomeIndexToCopy] )

			self.genomes[g].ID = self.nextAvailableID

			self.nextAvailableID = self.nextAvailableID + 1

                        self.genomes[g].Mutate()

                        self.genomes[g].Reset()
