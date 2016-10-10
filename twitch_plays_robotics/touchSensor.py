import constants
import numpy as np
import copy

class TOUCH_SENSOR:

        def __init__(self, ID = 0 ,objectIndex = 0 ,simulator = None):

                self.ID = ID

                self.objectIndex = objectIndex

		simulator.Send_Touch_Sensor(ID = self.ID , objectIndex = self.objectIndex)

	def Get_Data_From_Simulator(self, simulator):

		self.values = copy.deepcopy(simulator.Get_Sensor_Data(self.ID,0))

	def Get_Value(self):

		return np.mean(self.values)
