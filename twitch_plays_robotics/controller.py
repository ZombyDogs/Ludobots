import constants
import numpy as np
import constants as c
import random
import math

class CONTROLLER:

        def __init__(self):

		self.synapses = np.random.rand( c.NUM_SENSOR_NEURONS + c.NUM_HIDDEN_NEURONS , c.NUM_HIDDEN_NEURONS + c.NUM_MOTOR_NEURONS) * 2 - 1

		self.sensorTaus = np.random.rand( c.NUM_SENSOR_NEURONS )

                self.hiddenTaus = np.random.rand( c.NUM_HIDDEN_NEURONS )

                self.motorTaus = np.random.rand( c.NUM_MOTOR_NEURONS )

        def Get_Hidden_Tau(self,h):

                return self.hiddenTaus[h]

        def Get_Motor_Tau(self,m):

                return self.motorTaus[m]

	def Get_Sensor_Tau(self,s):

		return self.sensorTaus[s]

	def Get_Synapse(self,i,j):

		return self.synapses[i,j]

	def Mutate(self):

		mutationType = random.randint(0,3)

		if ( mutationType == 0 ):

			self.Mutate_Synapse()

		elif ( mutationType == 1 ):

			self.Mutate_Sensor_Tau()

                elif ( mutationType == 2 ):

                        self.Mutate_Hidden_Tau()

                elif ( mutationType == 3 ):

                        self.Mutate_Motor_Tau()

        def Mutate_Hidden_Tau(self):

                j = random.randint(0, c.NUM_HIDDEN_NEURONS - 1 )

                self.hiddenTaus[j] = random.gauss( self.hiddenTaus[j] , math.fabs(self.hiddenTaus[j]) )

                if ( self.hiddenTaus[j] < c.TAU_MIN_VALUE ):

                        self.hiddenTaus[j] = c.TAU_MIN_VALUE

        def Mutate_Motor_Tau(self):

                j = random.randint(0, c.NUM_MOTOR_NEURONS - 1 )

                self.motorTaus[j] = random.gauss( self.motorTaus[j] , math.fabs(self.motorTaus[j]) )

                if ( self.motorTaus[j] < c.TAU_MIN_VALUE ):

                        self.motorTaus[j] = c.TAU_MIN_VALUE

	def Mutate_Sensor_Tau(self):

		j = random.randint(0, c.NUM_SENSOR_NEURONS - 1 )

		self.sensorTaus[j] = random.gauss( self.sensorTaus[j] , math.fabs(self.sensorTaus[j]) )

		if ( self.sensorTaus[j] < c.TAU_MIN_VALUE ):

			self.sensorTaus[j] = c.TAU_MIN_VALUE

	def Mutate_Synapse(self):

        	i = random.randint(0, c.NUM_SENSOR_NEURONS + c.NUM_HIDDEN_NEURONS - 1 )

        	j = random.randint(0, c.NUM_HIDDEN_NEURONS + c.NUM_MOTOR_NEURONS - 1 )

        	while ( ( i < c.NUM_SENSOR_NEURONS ) & ( j > c.NUM_HIDDEN_NEURONS ) ):

                	# No synapses from sensor to motor neurons allowed...

                	j = random.randint(0, c.NUM_HIDDEN_NEURONS + c.NUM_MOTOR_NEURONS - 1 )

        	self.synapses[i,j] = random.gauss(self.synapses[i,j],math.fabs(self.synapses[i,j]))
