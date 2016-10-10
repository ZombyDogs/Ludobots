import numpy as np
import constants as c
from box import BOX

class ENVIRONMENT:

	def __init__(self):

		self.boxes = {}

		for b in range(0,c.numBoxes):

			self.boxes[b] = BOX()

        def Send_To(self,simulator):

		for b in range(0,c.numBoxes):

			self.boxes[b].Send_To(simulator)
