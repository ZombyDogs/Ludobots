from simulator import SIMULATOR
import random

parent = SIMULATOR()

for i in range(0,10):

	parent.Send_Box( x = random.random() , y = random.random() , z = random.random()*5 )

	parent.Send_Touch_Sensor(i)

parent.Start()

