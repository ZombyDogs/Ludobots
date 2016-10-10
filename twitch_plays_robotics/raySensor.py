import math
import constants
import numpy as np
import copy

class RAY_SENSOR:

	def __init__(self,ID,object,simulator):

                self.ID = ID

		simulator.Send_Ray_Sensor(ID=self.ID, objectIndex = object.ID, x=object.x, y=object.y, z=object.z, r1=object.r1, r2=object.r2, r3=object.r3)

	def Get_Data_From_Simulator(self, simulator):

		self.distances = copy.deepcopy(simulator.Get_Sensor_Data(self.ID,0))

               	self.r = copy.deepcopy(simulator.Get_Sensor_Data(self.ID,1))

               	self.g = copy.deepcopy(simulator.Get_Sensor_Data(self.ID,2))

               	self.b = copy.deepcopy(simulator.Get_Sensor_Data(self.ID,3))

        def Get_Amount_Of_Blue(self):

                return 1.0 / (1.0 + math.sqrt( math.pow(np.mean(self.r)-0,2.0) + math.pow(np.mean(self.g)-0,2.0) + math.pow(np.mean(self.b)-1,2.0) ) )

        def Get_Amount_Of_Green(self):

                return 1.0 / (1.0 + math.sqrt( math.pow(np.mean(self.r)-0,2.0) + math.pow(np.mean(self.g)-1,2.0) + math.pow(np.mean(self.b)-0,2.0) ) )

	def Get_Amount_Of_Red(self):

                return 1.0 / (1.0 + math.sqrt( math.pow(np.mean(self.r)-1,2.0) + math.pow(np.mean(self.g)-0,2.0) + math.pow(np.mean(self.b)-0,2.0) ) )

        def Get_Amount_Of_White(self):

                return 1.0 / (1.0 + math.sqrt( math.pow(np.mean(self.r)-1,2.0) + math.pow(np.mean(self.g)-1,2.0) + math.pow(np.mean(self.b)-1,2.0) ) )

	def Get_Distance(self):

		return np.mean(self.distances)
