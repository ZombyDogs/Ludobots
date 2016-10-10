from simulator import SIMULATOR

simulator = SIMULATOR(showGraphics=True)

simulator.Send('Box                0 0 0.25            0.1 0.1 0.5         \n')

simulator.Send('Box                0 0.25 0.5          0.1 0.5 0.1         \n')

simulator.Send('Joint 0 1          0 0 0.5             1 0 0 \n')

simulator.Send('Done')
