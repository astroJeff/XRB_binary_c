import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.gridspec as gridspec

import corner
import pickle

import binary_c
import xrb
import xrb.src.constants as c
from xrb.binary import binary_evolve
from xrb.src import stats
from xrb.SF_history import sf_history
from xrb.pop_synth import pop_synth


from xrb.src.core import *
set_data_path("../data")




c.sf_scheme = "SMC"

start = time.time()

chains, HMXB_derived = stats.run_emcee_population(nburn=20000, nsteps=200000, nwalkers=80, binary_scheme='binary_c',
                                                  return_sampler=False, print_progress=True)

end = time.time()

print "Elapsed time:", int((end-start)/3600), "hours and", (end-start)%3600.0, "seconds"


np.save("../data/SMC_chains.npy", chains)
np.save("../data/SMC_derived.npy", HMXB_derived)
