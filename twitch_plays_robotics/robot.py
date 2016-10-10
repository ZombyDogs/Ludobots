from bodyPart import BODY_PART
import constants as c

class ROBOT:

	def __init__(self):

		self.bodyParts = {}

		for b in range(0,c.numBodyParts):

			self.bodyParts[b] = BODY_PART()

        def Distance_To_The_Origin(self):

                distance = 0.0

                for b in range(0,c.numBodyParts):

                        distance = distance + self.bodyParts[b].Distance_To_The_Origin()

                return distance

	def Get_Sensor_Data_From(self,simulator):

		for b in range(0,c.numBodyParts):

			self.bodyParts[b].Get_Sensor_Data_From(simulator)

	def Mutate(self):

                for b in range(0,c.numBodyParts):

			self.bodyParts[b].Mutate()

        def Send_To(self,simulator):

                for b in range(0,c.numBodyParts):

                        self.bodyParts[b].Send_To(simulator)
