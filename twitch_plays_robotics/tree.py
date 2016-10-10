import constants as c
import copy
import math
import os
import simulator
import random
import pickle
import numpy as np

from node import NODE
from simulator import SIMULATOR

class TREE:

	def __init__(self):

                self.root = NODE(0,c.maxDepth,1,0.0,0.0,0,0,0)

		self.Create_Mirror_Image()

		self.Assign_IDs()

		self.Move_Up()

		self.sensorTaus = [] 

                self.hiddenTaus = []

                self.motorTaus = []

		self.shWeights = []

		self.hhWeights = []

		self.hmWeights = []

		self.color = np.random.random(3)

	def Add_External_Light_Source(self,nextAvailableID):

        	self.simulator.Send_Box(ID = nextAvailableID, x=0, y=+8, z=0.25, length=0.5, width=0.5, height=0.5, r=1, g=0, b=0)

                self.simulator.Send_Light_Source( objectIndex = nextAvailableID )

                self.simulator.Send_Box(ID = nextAvailableID + 1 , x=8, y=0, z=0.25, length=0.5, width=0.5, height=0.5, r=0, g=1, b=0)

                self.simulator.Send_Box(ID = nextAvailableID + 2, x=-8, y=0, z=0.25, length=0.5, width=0.5, height=0.5, r=0, g=0, b=1)

                self.simulator.Send_Box(ID = nextAvailableID + 3, x=0, y=-8, z=0.25, length=0.5, width=0.5, height=0.5, r=1, g=1, b=1)

	def Assign_IDs(self):

		self.ID = {}

		self.ID[0] = -1

		self.root.Assign_IDs(self.ID)

	def Compute_Fitness(self,whatToMaximize):

		if ( whatToMaximize == c.maximizeTouch ):

			self.fitness = -self.Sum_Touches()

		elif ( whatToMaximize == c.maximizeProprioception ):

			self.fitness = -self.Sum_Angles()

		elif ( whatToMaximize == c.maximizeHeight ):

			self.fitness = -self.Sum_Heights()

		elif ( whatToMaximize == c.maximizeLight ):

                        self.fitness = -self.Sum_Light()

                elif ( whatToMaximize == c.maximizeRed ):

                        self.fitness = -self.Sum_Red()

                elif ( whatToMaximize == c.maximizeGreen ):

                        self.fitness = -self.Sum_Green()

                elif ( whatToMaximize == c.maximizeBlue ):

                        self.fitness = -self.Sum_Blue()

                elif ( whatToMaximize == c.maximizeWhite ):

                        self.fitness = -self.Sum_White()

                elif ( whatToMaximize == c.maximizeVestibular ):

                        self.fitness = +self.Sum_Vestibular()

		else: # Maximize distance

			self.fitness = -self.Sum_Distances()

	def Create_Mirror_Image(self):

                self.root.children[1] = copy.deepcopy( self.root.children[0] )

		self.root.children[1].Reset()

                self.root.numChildren = 2

                self.root.children[1].Flip()

	def Evaluate(self,whatToMaximize):

        	self.Wait_To_Finish()

        	self.Get_Sensor_Data_From_Simulator()

		del self.simulator

		self.Compute_Fitness(whatToMaximize)

	def Get_Sensor_Data_From_Simulator(self):

		self.root.Get_Sensor_Data_From_Simulator(self.simulator)

	def Load(self):

		f = open('best.txt','rb')

		self = pickle.load(f)

		f.close()

	def Move_Up(self):

		lowestPoint = [1000.0]

		self.root.Find_Lowest_Point(lowestPoint)

		self.root.Move( 0 , 0, -lowestPoint[0] + c.radius )

	def Mutate(self):

		mutType = random.randint(0,1)

		if ( mutType == 0 ):

			self.Mutate_Body()
		else:
			self.Mutate_Brain()

                self.Create_Mirror_Image()

                self.Assign_IDs()

                self.Move_Up()

	def Mutate_Body(self):

		numberOfSegments = self.root.children[0].Count_Number_Of_Segments()

		segmentToMutate = random.randint(-1,numberOfSegments-2)

		self.root.children[0].Mutate(segmentToMutate)

		self.root.children[0].Update_Positions(self.root.x,self.root.y,self.root.z)

	def Mutate_Brain(self):

		mutType = random.randint(0,5)

		if ( mutType == 0 ):

			s = random.randint(0, self.sensorTaus.size-1)

			self.sensorTaus[s] = random.gauss( self.sensorTaus[s] , math.fabs(self.sensorTaus[s]) )

			if ( self.sensorTaus[s] > c.TAU_MAX ):

				self.sensorTaus[s] = c.TAU_MAX

                        if ( self.sensorTaus[s] < -c.TAU_MAX ):

                                self.sensorTaus[s] = -c.TAU_MAX

		elif ( mutType == 1 ):

                	h = random.randint(0, self.hiddenTaus.size-1)

                	self.hiddenTaus[h] = random.gauss( self.hiddenTaus[h] , math.fabs(self.hiddenTaus[h]) )

                        if ( self.hiddenTaus[h] > c.TAU_MAX ):

                                self.hiddenTaus[h] = c.TAU_MAX

                        if ( self.hiddenTaus[h] < -c.TAU_MAX ):

                                self.hiddenTaus[h] = -c.TAU_MAX

		elif ( mutType == 2 ):

                	m = random.randint(0, self.motorTaus.size-1)

                	self.motorTaus[m] = random.gauss( self.motorTaus[m] , math.fabs(self.motorTaus[m]) )

                        if ( self.motorTaus[m] > c.TAU_MAX ):

                                self.motorTaus[m] = c.TAU_MAX

                        if ( self.motorTaus[m] < -c.TAU_MAX ):

                                self.motorTaus[m] = -c.TAU_MAX

		elif ( mutType == 3 ):

                	s = random.randint(0, self.sensorTaus.size-1)

                	h = random.randint(0, self.hiddenTaus.size-1)

			self.shWeights[s,h] = random.gauss( self.shWeights[s,h] , math.fabs(self.shWeights[s,h]) )

		elif ( mutType == 4 ):

                	h1 = random.randint(0, self.hiddenTaus.size-1)

                	h2 = random.randint(0, self.hiddenTaus.size-1)

                	self.hhWeights[h1,h2] = random.gauss( self.hhWeights[h1,h2] , math.fabs(self.hhWeights[h1,h2]) )

		elif ( mutType == 5 ):

                	h = random.randint(0, self.hiddenTaus.size-1)

                	m = random.randint(0, self.motorTaus.size-1)

                	self.hmWeights[h,m] = random.gauss( self.hmWeights[h,m] , math.fabs(self.hmWeights[h,m]) )


	def Print(self):

		self.root.Print()

	def Save(self):

		f = open('tmp.txt','wb')

		pickle.dump(self,f)

		f.close()

		os.rename('tmp.txt','best.txt')

	def Send_Brain_To_Simulator(self,sensorsCreated,jointsCreated):

		self.Send_Neurons_To_Simulator(sensorsCreated,jointsCreated)

		self.Send_Synapses_To_Simulator(sensorsCreated,jointsCreated)

	def Send_Neurons_To_Simulator(self,sensorsCreated,jointsCreated):

		if ( self.sensorTaus == [] ):

			self.sensorTaus = np.random.rand(sensorsCreated[0])*2*c.TAU_MAX - c.TAU_MAX
		
		for s in range(0,sensorsCreated[0]):

			self.simulator.Send_Sensor_Neuron(ID=s, sensorID=s, sensorValueIndex=0, layer=0, tau=self.sensorTaus[s] )
	
                if ( self.hiddenTaus == [] ):

                        self.hiddenTaus = np.random.rand(c.NUM_HIDDEN_NEURONS)*2*c.TAU_MAX - c.TAU_MAX
	
		for h in range(0,c.NUM_HIDDEN_NEURONS):

			self.simulator.Send_Hidden_Neuron(ID= sensorsCreated[0] + h, layer=1, tau=self.hiddenTaus[h] )

                if ( self.motorTaus == [] ):

                        self.motorTaus = np.random.rand(jointsCreated[0])*2*c.TAU_MAX - c.TAU_MAX

		for m in range(0,jointsCreated[0]):

			self.simulator.Send_Motor_Neuron(ID = sensorsCreated[0] + c.NUM_HIDDEN_NEURONS + m , jointID = m , layer = 2 , tau = self.motorTaus[m] )

	def Send_Synapses_To_Simulator(self,sensorsCreated,jointsCreated):

		if ( self.shWeights == [] ):

			self.shWeights = np.random.rand(sensorsCreated[0],c.NUM_HIDDEN_NEURONS) * 2 - 1

		for s in range(0,sensorsCreated[0]):

			for h in range(0,c.NUM_HIDDEN_NEURONS):

				self.simulator.Send_Synapse( sourceNeuronIndex = s , targetNeuronIndex = sensorsCreated[0] + h , weight = self.shWeights[s,h] )


                if ( self.hhWeights == [] ):

                        self.hhWeights = np.random.rand(c.NUM_HIDDEN_NEURONS,c.NUM_HIDDEN_NEURONS) * 2 - 1

		for h1 in range(0,c.NUM_HIDDEN_NEURONS):

			for h2 in range(0,c.NUM_HIDDEN_NEURONS):

				self.simulator.Send_Synapse( sourceNeuronIndex = sensorsCreated[0] + h1 , targetNeuronIndex = sensorsCreated[0] + h2 , weight = self.hhWeights[h1,h2] )


                if ( self.hmWeights == [] ):

                        self.hmWeights = np.random.rand(c.NUM_HIDDEN_NEURONS,jointsCreated[0]) * 2 - 1

		for h in range(0,c.NUM_HIDDEN_NEURONS):

			for m in range(0,jointsCreated[0]):

                                self.simulator.Send_Synapse( sourceNeuronIndex = sensorsCreated[0] + h , targetNeuronIndex = sensorsCreated[0] + c.NUM_HIDDEN_NEURONS + m , weight = self.hmWeights[h,m] )


	def Send_To_Simulator(self,playBlind,playPaused,evaluationTime):

		self.simulator = SIMULATOR(playBlind,playPaused,evaluationTime)

		sensorsCreated = {}

		sensorsCreated[0] = 0

		self.root.Send_Objects_To_Simulator(self.simulator,sensorsCreated,self.color)

		self.Add_External_Light_Source(self.root.Number_Of_Nodes()-1)

		jointsCreated = {}

		jointsCreated[0] = 0

		self.root.Send_Joints_To_Simulator(self.simulator,jointsCreated,sensorsCreated)

		self.Send_Brain_To_Simulator(sensorsCreated,jointsCreated)

		self.simulator.Start()

        def Sum_Angles(self):

                return self.root.Sum_Angles()

        def Sum_Blue(self):

                return self.root.Sum_Blue()

	def Sum_Distances(self):

		return self.root.Sum_Distances()

        def Sum_Green(self):

                return self.root.Sum_Green()

	def Sum_Heights(self):

		return self.root.Sum_Heights()

	def Sum_Light(self):

		return self.root.Sum_Light()

	def Sum_Red(self):

		return self.root.Sum_Red()

	def Sum_Touches(self):

		return self.root.Sum_Touches()

        def Sum_White(self):

		return self.root.Sum_White()

	def Sum_Vestibular(self):

		return self.root.Sum_Vestibular()

	def Wait_To_Finish(self):

		self.simulator.Wait_To_Finish()
