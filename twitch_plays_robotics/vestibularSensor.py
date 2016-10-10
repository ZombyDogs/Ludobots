import constants

import numpy as np

import copy

class VESTIBULAR_SENSOR:

        def __init__(self, ID = 0 ,objectIndex = 0 ,simulator = None):

                self.ID = ID

                self.objectIndex = objectIndex

		simulator.Send_Vestibular_Sensor(ID=self.ID , objectIndex=self.objectIndex)

	def Get_Data_From_Simulator(self, simulator):

               	self.angles = copy.deepcopy(simulator.Get_Sensor_Data(self.ID,0))

	def Get_Angle(self):

		return np.mean(self.angles)
