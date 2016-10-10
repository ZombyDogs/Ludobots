import random
import math
from positionSensor import POSITION_SENSOR

class BODY_PART:

	def __init__(self):

		self.x = random.random()
		self.y = random.random()
		self.z = random.random()

		# self.length = 0.1
		# self.width = 0.1
		# self.height = 0.1

		self.length = 0.0
		self.radius = 0.1

		self.positionSensor = POSITION_SENSOR()

        def Distance_To_The_Origin(self):

                return math.sqrt( math.pow(self.x,2.0) + math.pow(self.y,2.0) )

	def Encode_As_String(self):

                # stringToSend = 'Box\n'

		stringToSend = 'Cylinder\n'

                stringToSend = stringToSend + str(self.x) + '\n'

                stringToSend = stringToSend + str(self.y) + '\n'

                stringToSend = stringToSend + str(self.z) + '\n'

                stringToSend = stringToSend + str(self.length) + '\n'

                #stringToSend = stringToSend + str(self.width) + '\n'
                #stringToSend = stringToSend + str(self.height) + '\n'

                stringToSend = stringToSend + str(self.radius) + '\n'

                return( stringToSend )

	def Get_Sensor_Data_From(self,simulator):

                capturedText = simulator.Get()

                pos = capturedText.split()

                self.x = float(pos[0])
                self.y = float(pos[1])
                self.z = float(pos[2])

	def Mutate(self):

		self.x = random.gauss( self.x , math.fabs(self.x) )

                self.y = random.gauss( self.y , math.fabs(self.y) )

                self.z = random.gauss( self.z , math.fabs(self.z) )

	def Print(self):

		print self.Encode_As_String()

	def Send_To(self,simulator):

                simulator.Send( self.Encode_As_String() )

