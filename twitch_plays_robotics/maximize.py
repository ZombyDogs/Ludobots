from afpo import AFPO

import sys

whatToMaximize = sys.argv[1]

afpo = AFPO(whatToMaximize)

afpo.Evolve()

