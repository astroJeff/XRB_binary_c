import numpy as np
import pickle

import binary_c
import xrb
import xrb.src.constants as c
from xrb.binary import binary_evolve
from xrb.src import stats
from xrb.SF_history import sf_history
from xrb.pop_synth import pop_synth
from xrb.models import HMXB


from xrb.src.core import *
set_data_path("../data")


# Set up parameters
c.sf_scheme = "SMC"
metallicity = 0.008

start = time.time()


# Number of systems per time slice
N = 50000

# Empty array for input binary parameters
x_i_good = np.empty((0, 11))

# Loop through times
for t_b in np.linspace(5.0, 60.0, 221):

    print "t_b:", t_b

    # Get initial binary parameters
    x_i = pop_synth.generate_population(N)

    # From t_b, get coordinates
    ra_i, dec_i, N_stars = pop_synth.get_random_positions(N, t_b)

    # Run each system individually
    for i in np.arange(N):

        M1 = x_i[0][i]
        M2 = x_i[1][i]
        A = x_i[2][i]
        ecc = x_i[3][i]
        v_k = x_i[4][i]
        theta_k = x_i[5][i]
        phi_k = x_i[6][i]
        ra = ra_i[i]
        dec = dec_i[i]

        orbital_period = binary_evolve.A_to_P(M1, M2, A)



        # Run binary_c
        output = binary_c.run_binary(M1, M2, orbital_period, ecc, metallicity, t_b, v_k,
                                     theta_k, phi_k, v_k, theta_k, phi_k, 0, 1)

        # Add system to output array if it is an HMXB
        if HMXB.check_output(output, binary_type="HMXB"):
            x_i_good = np.concatenate((x_i_good, np.array([[M1, M2, A, ecc, v_k, theta_k, phi_k, ra, dec, t_b, N_stars]])), axis=0)


end = time.time()
print "Elapsed time:", int((end-start)/3600), "hours and", (end-start)%3600.0, "seconds"


np.save("../data/SMC_forward.npy", x_i_good)
