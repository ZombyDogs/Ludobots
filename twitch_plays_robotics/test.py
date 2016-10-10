from genome import GENOME
import constants as c
import copy

parent = GENOME(0)

parent.Send_To_Simulator(playBlind=True,playPaused=False,evaluationTime=2)

parent.Get_From_Simulator(c.maximizeHeight)

for g in range(0,1000):

	child = copy.deepcopy(parent)

	child.Mutate()

	child.Send_To_Simulator(playBlind=True,playPaused=False,evaluationTime=2)

	child.Get_From_Simulator(c.maximizeHeight)

	print g, parent.fitness , child.fitness

	if ( child.fitness < parent.fitness ):

		parent = child

parent.Send_To_Simulator(playBlind=False,playPaused=True,evaluationTime=100)

