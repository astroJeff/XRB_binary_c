import numpy as np
import time
import pickle

import xrb
import binary_c

from xrb.src.core import *
from xrb.src import stats

start = time.time()

c.SF_scheme='LMC'

sampler = stats.run_emcee_population(nburn=2, nsteps=, nwalkers=80, binary_scheme='binary_c')

end = time.time()


print "Elapsed time:", end-start, "seconds" 


pickle.dump(sampler, open("../data/LMC_sampler.obj")) 


