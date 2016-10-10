import constants
import numpy as np
import copy

class POSITION_SENSOR:

	def __init__(self, ID = 0 ,objectIndex = 0 ,simulator = None):

		self.ID = ID

		self.objectIndex = objectIndex

		self.simulator = simulator

		simulator.Send_Position_Sensor(ID=self.ID,objectIndex=self.objectIndex)

	def Get_Data_From_Simulator(self, simulator):

               	self.x = copy.deepcopy(simulator.Get_Sensor_Data(self.ID,0))

               	self.y = copy.deepcopy(simulator.Get_Sensor_Data(self.ID,1))

               	self.z = copy.deepcopy(simulator.Get_Sensor_Data(self.ID,2))

	def Get_Height(self):

		return np.mean(self.z)
