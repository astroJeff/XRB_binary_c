from xrb.src.core import *
from xrb.models import HMXB

import emcee




nwalkers = 80
nburn = 1000
nrun = 10000


p0 = np.zeros((nwalkers,8))

m1_set = np.random.normal(loc=10, size=nwalkers)
m2_set = np.random.normal(loc=10, size=nwalkers)
A_set = np.random.normal(loc=100, size=nwalkers)
e_set = np.random.normal(loc=0.5, scale=0.1, size=nwalkers)
v_k_1_set = np.random.normal(loc=100, size=nwalkers)
theta_1_set = np.random.normal(loc=1, scale=0.1, size=nwalkers)
phi_1_set = np.random.normal(loc=1, scale=0.1, size=nwalkers)
time_set = np.random.normal(loc=20, size=nwalkers)


p0[:,0] = m1_set
p0[:,1] = m2_set
p0[:,2] = A_set
p0[:,3] = e_set
p0[:,4] = v_k_1_set
p0[:,5] = theta_1_set
p0[:,6] = phi_1_set
p0[:,7] = time_set



sampler = emcee.EnsembleSampler(nwalkers=nwalkers, dim=8, lnpostfn=HMXB.ln_priors_population)


# Burn-in
print "Starting burn-in..."
pos,prob,state = sampler.run_mcmc(p0, N=nburn)
print "...finished running burn-in"

# Full run
print "Starting full run..."
sampler.reset()
pos,prob,state = sampler.run_mcmc(pos, N=nrun)
print "...full run finished"



chains = sampler.chain
np.save("../data/prior_chains.npy", chains)
