import numpy as np
import time
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
 
import corner

import xrb
import binary_c

from xrb.src.core import *
from xrb.src import stats
from xrb.SF_history import sf_history


from matplotlib import font_manager
import matplotlib.gridspec as gridspec

start = time.time()

c.sf_scheme='LMC'

sampler = stats.run_emcee_population(nburn=1000, nsteps=2000, nwalkers=80, binary_scheme='binary_c')

end = time.time()


print "Elapsed time:", end-start, "seconds" 


pickle.dump(sampler, open("../data/LMC_sampler.obj", "wb")) 





# Generate corner plot

# Corner plot
fontProperties = {'family':'serif', 'serif':['Times New Roman'], 'weight':'normal', 'size':12}
ticks_font = font_manager.FontProperties(family='Times New Roman', style='normal', \
                                         weight='normal', stretch='normal', size=12)
plt.rc('font', **fontProperties)

fig, ax = plt.subplots(10,10, figsize=(10,10))


labels = [r"$M_{\rm 1, i}\ (M_{\odot})$", r"$M_{\rm 2, i}\ (M_{\odot})$", r"$a_{\rm i}\ (R_{\odot})$", \
          r"$e_{\rm i}$", r"$v_{\rm k, i}\ ({\rm km}\ {\rm s}^{-1})$", r"$\theta_{\rm k}\ ({\rm rad.})$", \
          r"$\phi_{\rm k}\ ({\rm rad.})$", r"$\alpha_{\rm i}\ ({\rm deg.})$", \
          r"$\delta_{\rm i}\ ({\rm deg.}) $", r"$t_{\rm i}\ ({\rm Myr})$"]
plt_range = ([0,35], [0,22], [0,5900], [0,1], [0,1200], [0,np.pi], [0,np.pi], [70,90], [-72,-65], [0,200])

hist2d_kwargs = {"plot_datapoints" : False}
fig = corner.corner(sampler.flatchain, fig=fig, labels=labels, range=plt_range, max_n_ticks=4, **hist2d_kwargs)
# fig = corner.corner(sampler.flatchain, fig=fig, labels=labels, max_n_ticks=4, **hist2d_kwargs)

ra_out = sampler.flatchain.T[7]
dec_out = sampler.flatchain.T[8]
gs = gridspec.GridSpec(2, 2,
                       width_ratios=[3,2],
                       height_ratios=[2,3]
                       )
smc_plot, ax1 = sf_history.get_plot_polar(20, fig_in=fig, gs=gs[1], ra_dist=ra_out, dec_dist=dec_out, \
                                          dist_bins=30, xgrid_density=6)


ax1.set_position([0.55, 0.55, 0.3, 0.3])


# Shift axis labels
for i in np.arange(10):
    ax[i,0].yaxis.set_label_coords(-0.5, 0.5)
    ax[9,i].xaxis.set_label_coords(0.5, -0.5)


plt.subplots_adjust(bottom=0.07, left=0.07, top=0.97)


plt.savefig('../figures/population_lmc.pdf', rasterized=True)
# plt.show()

