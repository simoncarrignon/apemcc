from sampler import *
from abcpmc import LinearEps
import numpy as np
import sys,os

from model.apemcc import CCSimu
from data.ceramic import *

### if use with MPI
#from abcpmc import mpi_util

pref=sys.argv[1] #a prefix that will be used as a folder to store the result of the ABC
#
if not os.path.exists(pref):
    os.makedirs(pref)


#distance function: sum of abs mean differences, we take Y (the evidenceS) as a list of percentage of the same sie than x but with value .95. _ie_ our evidence are a theoretical case where all the goods are at 95% of the same type during all the years
def dist(x, y):
    #for w in x.keys():
    #    for measurment in x[w].production.keys():
    #        allm=x[w].production[measurment]
    #        realsummary=data['mean'][w][measurment]
    #        realsummary-np.mean(allm)
    alldist=[]
    if len(x)<len(y['sd'].keys()):
        return(10000)
    for w in x.keys():
        allm=x[w].production["rim_w"]
        realsummary=data['mean'][w]["rim_w"]
        realsummary=np.mean(allm[len(allm)-10:])
        alldist.append(abs(realsummary-np.mean(allm)))
    return np.mean(alldist)

#our "model", a gaussian with varying means
def postfn(theta):
    # we reject the particul with no credible parameters (ie pop < 0 etc...)
    if(theta[0]>1 or theta[1]<0 or theta[1]>1 or theta[0]<0):
        return([-10000])
    else:
        p_mu=theta[0]
        p_copy=theta[1]
        ## we fixed the number of time step and we look only at three parameter: posize copy and mutation
        exp=CCSimu(-1,3000,pref,-1,p_mu,p_copy,0,"file",dist_list=realdist,outputfile=False,mu_str=realsd,log=False)
        return exp.run()

data={'sd':allsds,'mean':allmeans}  #we dont use it in this expe

eps = LinearEps(10, 10, 0.115)
prior = TophatPrior([0,0],[1,1])

### if used with MPI
#mpi_pool = mpi_util.MpiPool()
#sampler = abcpmc.Sampler(N=100, Y=data, postfn=postfn, dist=dist,pool=mpi_pool) 
###

sampler = Sampler(N=200, Y=data, postfn=postfn, dist=dist)

for pool in sampler.sample(prior, eps):
    print("T:{0},eps:{1:>.4f},ratio:{2:>.4f}".format(pool.t, pool.eps, pool.ratio))
    for i, (mean, std) in enumerate(zip(np.mean(pool.thetas, axis=0), np.std(pool.thetas, axis=0))):
        print(u"    theta[{0}]: {1:>.4f} \u00B1 {2:>.4f}".format(i, mean,std))

    np.savetxt(pref+"/result_"+str(pool.eps)+".csv", pool.thetas, delimiter=",",fmt='%1.5f',comments="")
    #np.savetxt(bias+"/result_"+str(pool.eps)+".csv", pool.thetas, delimiter=",",header="n_agents,time,p_mu,p_copy",fmt='%1.5f',comments="")

