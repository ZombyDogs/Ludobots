import random

class BOX:

	def __init__(self):

		self.x = random.random()
		self.y = random.random()
		self.z = random.random()

	def Encode_As_String(self):

                stringToSend = 'Box '

                stringToSend = stringToSend + str(self.x) + ' '

                stringToSend = stringToSend + str(self.y) + ' '

                stringToSend = stringToSend + str(self.z) + ' '

                return( stringToSend )

	def Send_To(self,simulator):

                simulator.Send( self.Encode_As_String() )

