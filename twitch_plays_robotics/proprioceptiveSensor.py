import constants
import numpy as np
import copy

class PROPRIOCEPTIVE_SENSOR:

        def __init__(self, ID = 0 ,jointIndex = 0 ,simulator = None):

                self.ID = ID

                self.jointIndex = jointIndex

                simulator.Send_Proprioceptive_Sensor( ID = self.ID , jointIndex = self.jointIndex )

	def Get_Data_From_Simulator(self, simulator):

		self.angles = copy.deepcopy(simulator.Get_Sensor_Data(self.ID,0))

	def Get_Value(self):

		# return self.angles[0]

		return np.mean(self.angles)
