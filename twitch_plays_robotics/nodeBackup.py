import constants
import math
import random
import simulator
import numpy as np
from positionSensor import POSITION_SENSOR
from proprioceptiveSensor import PROPRIOCEPTIVE_SENSOR
from touchSensor import TOUCH_SENSOR
from raySensor import RAY_SENSOR
from lightSensor import LIGHT_SENSOR
from vestibularSensor import VESTIBULAR_SENSOR

class NODE:

	def __init__(self,myDepth,maxDepth,numChildren,myAngle1,myAngle2,x,y,z):

		self.myDepth = myDepth

		self.numChildren = numChildren

		self.myAngle1 = myAngle1

		self.myAngle2 = myAngle2

		self.x = x

		self.y = y

		self.z = z

		self.positionSensor = None

		self.proprioceptiveSensor = None

		self.touchSensor = None

		self.raySensor = None

		self.lightSensor = None

		self.vestibularSensor = None

		self.children = {}

		if ( self.myDepth < maxDepth ):

			self.Create_Children(maxDepth)
		else:
			self.numChildren = 0

	def Assign_IDs(self,ID):

		self.ID = ID[0]

		ID[0] = ID[0] + 1

		for c in range(0,self.numChildren):

			self.children[c].Assign_IDs(ID)

        def Compute_Joint_Normal(self,object1,object2,object3):

                        P = np.zeros(3)
                        P[0] = object1.x
                        P[1] = object1.y
                        P[2] = object1.z

                        Q = np.zeros(3)
                        Q[0] = object2.x
                        Q[1] = object2.y
                        Q[2] = object2.z

                        R = np.zeros(3)
                        R[0] = object3.x
                        R[1] = object3.y
                        R[2] = object3.z

                        a = Q - P
                        b = R - P

                        return np.cross(a,b)

	def Count_Number_Of_Segments(self):

		numSegments = 0

		if ( self.ID >= 0 ):

			numSegments = numSegments + 1

		for c in range(0,self.numChildren):

			numSegments = numSegments + self.children[c].Count_Number_Of_Segments()

		return numSegments

	def Create_Children(self,maxDepth):

		for c in range(0,self.numChildren):

                       	hisAngle1 = self.myAngle1 + random.random()*2.0*3.14159 - 3.14159

                        hisAngle2 = self.myAngle2 + random.random()*2.0*3.14159 - 3.14159

                        hisX = self.x + constants.length * math.cos(hisAngle1) * math.sin(hisAngle2)

                        hisY = self.y + constants.length * math.sin(hisAngle1) * math.sin(hisAngle2)

                        hisZ = self.z + constants.length * math.cos(hisAngle2)

			self.children[c] = NODE(self.myDepth+1,maxDepth,constants.maxChildren,hisAngle1,hisAngle2,hisX,hisY,hisZ)

        def Create_Joints_In_Simulator(self,simulator,parent,jointsCreated,sensorsCreated):

		for c in range(0,self.numChildren):

			jointNormal = self.Compute_Joint_Normal(parent,self,self.children[c])

               		simulator.Send_Joint(ID = jointsCreated[0] , firstObjectID = self.ID, secondObjectID = self.children[c].ID, x = self.x, y = self.y, z = self.z, n1 = jointNormal[0], n2 = jointNormal[1], n3 = jointNormal[2], lo = -constants.JOINT_ANGLE_MAX, hi = +constants.JOINT_ANGLE_MAX)

			# self.proprioceptiveSensor = PROPRIOCEPTIVE_SENSOR(sensorsCreated,jointsCreated[0],simulator)

			jointsCreated[0] = jointsCreated[0] + 1

                        self.children[c].Create_Joints_In_Simulator(simulator,self,jointsCreated,sensorsCreated)

        def Create_Objects_In_Simulator(self,simulator,parentX,parentY,parentZ,sensorsCreated,color):

		x = (parentX + self.x) / 2.0
                y = (parentY + self.y) / 2.0
                z = (parentZ + self.z) / 2.0

		self.r1 = self.x - parentX
                self.r2 = self.y - parentY
                self.r3 = self.z - parentZ

		self.length = math.sqrt( math.pow(self.x - parentX,2.0) + math.pow(self.y - parentY,2.0) + pow(self.z - parentZ,2.0) )

		simulator.Send_Cylinder(ID = self.ID, x=x, y=y, z=z, r1=self.r1, r2=self.r2, r3=self.r3, length=self.length, radius=constants.radius,r=color[0],g=color[1],b=color[2])

		#self.positionSensor = POSITION_SENSOR( ID = sensorsCreated[0] , objectIndex = self.ID , simulator = simulator)
                #sensorsCreated[0] = sensorsCreated[0] + 1

		self.touchSensor = TOUCH_SENSOR( ID = sensorsCreated[0] , objectIndex = self.ID , simulator = simulator )
		sensorsCreated[0] = sensorsCreated[0] + 1

                self.lightSensor = LIGHT_SENSOR( ID = sensorsCreated[0] , objectIndex = self.ID , simulator = simulator)
                sensorsCreated[0] = sensorsCreated[0] + 1

		# testing
	
		if ( self.numChildren == 0 ):

			self.raySensor = RAY_SENSOR( ID = sensorsCreated[0] , object = self , simulator=simulator )
			sensorsCreated[0] = sensorsCreated[0] + 1

                #	self.vestibularSensor = VESTIBULAR_SENSOR(sensorsCreated,self.ID,simulator)

		for c in range(0,self.numChildren):

			self.children[c].Create_Objects_In_Simulator(simulator,self.x,self.y,self.z,sensorsCreated,color)

	def Find_Lowest_Point(self,lowestPoint):

		if ( self.z < lowestPoint[0] ):

			lowestPoint[0] = self.z

		for c in range(0,self.numChildren):

			self.children[c].Find_Lowest_Point(lowestPoint)

        def Find_Highest_Point(self,highestPoint):

		if ( self.ID >=0 ):
	
                	if ( self.finalZ > highestPoint[0] ):

                        	highestPoint[0] = self.finalZ

                for c in range(0,self.numChildren):

                        self.children[c].Find_Highest_Point(highestPoint)

	def Flip(self):

		self.x = -self.x

		for c in range(0,self.numChildren):

			self.children[c].Flip()

	def Get_Sensor_Data_From_Simulator(self,simulator):

                if ( self.raySensor ):

                        self.raySensor.Get_Data_From_Simulator(simulator)

                if ( self.lightSensor ):

                        self.lightSensor.Get_Data_From_Simulator(simulator)

		if ( self.positionSensor ):

			self.positionSensor.Get_Data_From_Simulator(simulator)

                if ( self.proprioceptiveSensor ):

                        self.proprioceptiveSensor.Get_Data_From_Simulator(simulator)

                if ( self.touchSensor ):

                        self.touchSensor.Get_Data_From_Simulator(simulator)

                if ( self.vestibularSensor ):

                        self.vestibularSensor.Get_Data_From_Simulator(simulator)

		for c in range(0,self.numChildren):

			self.children[c].Get_Sensor_Data_From_Simulator(simulator)

	def Make_Parent_Of(self,other):

		other.Recalculate_Depth(self.myDepth+1)

		self.children[self.numChildren] = other

		self.numChildren = self.numChildren + 1

	def Move(self,x,y,z):

		self.x = self.x + x

		self.y = self.y + y

		self.z = self.z + z

		for c in range(0,self.numChildren):

			self.children[c].Move(x,y,z)

        def Mutate(self,nodeIDToMutate):

                if ( self.ID == nodeIDToMutate):

                        # self.Mutate_Length()

			self.Mutate_Angles()
                else:
                        for c in range(0,self.numChildren):

                                self.children[c].Mutate(nodeIDToMutate)

	def Mutate_Angles(self):

		angle1Change = random.random()*0.1 - 0.05

		angle2Change = random.random()*0.1 - 0.05

		self.Update_Angles(angle1Change,angle2Change)

	def Mutate_Length(self):

		self.x = self.x + random.random()*0.1 - 0.05

                self.y = self.y + random.random()*0.1 - 0.05

                self.z = self.z + random.random()*0.1 - 0.05

	def Number_Of_Nodes(self):

		numNodes = 1

		for c in range(0,self.numChildren):

			numNodes = numNodes + self.children[c].Number_Of_Nodes()

		return numNodes
	
	def Print(self):

		outputString = ''

		for i in range(0,self.myDepth):

			outputString = outputString + '   '

		outputString = outputString + str(self.ID) + ' '

		outputString = outputString + str(self.x) + ' '

                outputString = outputString + str(self.y) + ' '

                outputString = outputString + str(self.z) + ' '

		print outputString

		for c in range(0,self.numChildren):

			self.children[c].Print()

	def Recalculate_Depth(self,myDepth):

		self.myDepth = myDepth

		for c in range(0,self.numChildren):
	
			self.children[c].Recalculate_Depth( self.myDepth + 1 )

	def Reset(self):

		self.positionSensor = None

		self.proprioceptiveSensor = None

		self.raySensor = None

		self.proprioceptiveSensor = None

		self.lightSensor = None

		self.ID = None

		for c in range(0,self.numChildren):

			self.children[c].Reset()

        def Send_Joints_To_Simulator(self,simulator,jointsCreated,sensorsCreated):

		jointNormal = self.Compute_Joint_Normal(self.children[0],self,self.children[1])

                simulator.Send_Joint(ID = jointsCreated[0] , firstObjectID = self.children[0].ID, secondObjectID = self.children[1].ID, x = self.x, y = self.y, z = self.z, n1 = jointNormal[0], n2 = jointNormal[1], n3 = jointNormal[2], lo = -constants.JOINT_ANGLE_MAX, hi = +constants.JOINT_ANGLE_MAX ) 

                # if ( self.proprioceptiveSensor ):

                #	self.proprioceptiveSensor = PROPRIOCEPTIVE_SENSOR(sensorsCreated,jointsCreated[0],simulator)

		jointsCreated[0] = jointsCreated[0] + 1

                for c in range(0,self.numChildren):

                        self.children[c].Create_Joints_In_Simulator(simulator,self,jointsCreated,sensorsCreated)

	def Send_Objects_To_Simulator(self,simulator,sensorsCreated,color):

		for c in range(0,self.numChildren):

			self.children[c].Create_Objects_In_Simulator(simulator,self.x,self.y,self.z,sensorsCreated,color)

        def Sum_Angles(self):

                sumOfAngles = 0

                if ( self.proprioceptiveSensor ):

                        sumOfAngles = self.proprioceptiveSensor.Get_Value()

                for c in range(0,self.numChildren):

                        sumOfAngles = sumOfAngles + self.children[c].Sum_Angles()

                return sumOfAngles

        def Sum_Blue(self):

                sumOfBlue = 0

                if ( self.raySensor ):

                        sumOfBlue = self.raySensor.Get_Amount_Of_Blue()

                for c in range(0,self.numChildren):

                        sumOfBlue = sumOfBlue + self.children[c].Sum_Blue()

                return sumOfBlue

        def Sum_Distances(self):

                sumOfDistances = 0

                if ( self.raySensor ):

                        sumOfDistances = self.raySensor.Get_Distance()

                for c in range(0,self.numChildren):

                        sumOfDistances = sumOfDistances + self.children[c].Sum_Distances()

                return sumOfDistances

        def Sum_Green(self):

                sumOfGreen = 0

                if ( self.raySensor ):

                        sumOfGreen = self.raySensor.Get_Amount_Of_Green()

                for c in range(0,self.numChildren):

                        sumOfGreen = sumOfGreen + self.children[c].Sum_Green()

                return sumOfGreen

	def Sum_Heights(self):

		sumOfHeights = 0

		if ( self.positionSensor ):

			sumOfHeights = self.positionSensor.Get_Height()

		for c in range(0,self.numChildren):

			sumOfHeights = sumOfHeights + self.children[c].Sum_Heights()

		return sumOfHeights

        def Sum_Light(self):

                sumOfLight = 0

                if ( self.lightSensor ):

                        sumOfLight = self.lightSensor.Get_Value()

                for c in range(0,self.numChildren):

                        sumOfLight = sumOfLight + self.children[c].Sum_Light()

                return sumOfLight

        def Sum_Red(self):

                sumOfRed = 0

                if ( self.raySensor ):

                        sumOfRed = self.raySensor.Get_Amount_Of_Red()

                for c in range(0,self.numChildren):

                        sumOfRed = sumOfRed + self.children[c].Sum_Red()

                return sumOfRed

        def Sum_Touches(self):

                sumOfTouches = 0

                if ( self.touchSensor ):

                        sumOfTouches = self.touchSensor.Get_Value()

                for c in range(0,self.numChildren):

                        sumOfTouches = sumOfTouches + self.children[c].Sum_Touches()

                return sumOfTouches

        def Sum_Vestibular(self):

                sumOfVestibular = 0

                if ( self.vestibularSensor ):

                        sumOfVestibular = self.vestibularSensor.Get_Angle()

                for c in range(0,self.numChildren):

                        sumOfVestibular = sumOfVestibular + self.children[c].Sum_Vestibular()

                return sumOfVestibular

        def Sum_White(self):

                sumOfWhite = 0

                if ( self.raySensor ):

                        sumOfWhite = self.raySensor.Get_Amount_Of_White()

                for c in range(0,self.numChildren):

                        sumOfWhite = sumOfWhite + self.children[c].Sum_White()

                return sumOfWhite


	def Update_Angles(self,angle1Change,angle2Change):

		self.myAngle1 = self.myAngle1 + angle1Change

		self.myAngle2 = self.myAngle2 + angle2Change

		for c in range(0,self.numChildren):

			self.children[c].Update_Angles(angle1Change,angle2Change)

	def Update_Positions(self,parentX,parentY,parentZ):

        	self.x = parentX + constants.length * math.cos(self.myAngle1) * math.sin(self.myAngle2)

                self.y = parentY + constants.length * math.sin(self.myAngle1) * math.sin(self.myAngle2)

                self.z = parentZ + constants.length * math.cos(self.myAngle2)

		for c in range(0,self.numChildren):

			self.children[c].Update_Positions(self.x,self.y,self.z)
