import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.gridspec as gridspec

import corner
import time
import pickle

import binary_c
import xrb
from xrb.binary import binary_evolve
from xrb.src import stats
from xrb.SF_history import sf_history

from xrb.src.core import *
set_data_path("../data")


sampler = pickle.load(open("../data/SMC_sampler.obj", "rb"))


N = len(sampler.flatchain)


evol_set = np.array([], dtype='S')

for i, sample in zip(np.arange(N), sampler.flatchain):

    if i > 10:
        break

    m1, m2, a, ecc, v_k, theta_k, phi_k, alpha, delta, time = sample
    P_orb = binary_evolve.A_to_P(m1, m2, a)


    m1_out, m2_out, A_out, e_out, v_sys, L_x_out, tsn1, tsn2, k1_out, k2_out, comenv_count, evol_hist = \
                    binary_c.run_binary(m1, m2, P_orb, ecc, 0.008, time, v_k, theta_k, phi_k, v_k, theta_k, phi_k)

    evol_steps = evol_hist.split("\n")
    # evol_steps = evol_steps["JEFF" in evol_steps]

    evol_line = ""
    for s in evol_steps:
        if s.find("JEFF") == 0:
            data = s.split(" ")
            k1_before, k2_before, k1_after, k2_after = data[2], data[3], data[11], data[12]

            evol_line = evol_line + "(" + str(k1_before) + "-" + str(k2_before) + ":" + str(k1_after) + "-" + str(k2_after) +  ")"

    evol_set = np.append(evol_set, evol_line)

print np.unique(evol_set, return_counts=True)
