from sampler import *
from threshold import *
import numpy as np
import sys,os

from model.apemcc import CCSimu
from data.ceramic import *
from scipy.stats import ttest_ind_from_stats



#distance function: sum of abs mean differences, we take Y (the evidenceS) as a list of percentage of the same sie than x but with value .95. _ie_ our evidence are a theoretical case where all the goods are at 95% of the same type during all the years
def dist(x, y):
    alldist=[]
    if len(x)<len(y['sd'].keys()):
        return(10000)
    for w in x.keys():
        allm=x[w].production["protruding_rim"]
        realmean=float(data['mean'][w]["protruding_rim"])
        realsd=float(data['sd'][w]["protruding_rim"])
        realsize=samplesize[w]
        sample=min(100,len(allm))
        lastm=allm[-sample:]
        simumean=np.mean(lastm)
        simusd=np.std(lastm)
        simusize=sample
        t,p=ttest_ind_from_stats(realmean,realsd,realsize,simumean,simusd,simusize,equal_var=False)
        alldist.append(1-p)
    return np.mean(alldist)

#our "model", a gaussian with varying means
def postfn(theta):
    print(theta)
    # we reject the particul with no credible parameters (ie pop < 0 etc...)
    #if(theta[0]>1 or theta[1]<0 or theta[1]>1 or theta[0]<0):
    if(theta[0]>1 or theta[3]<=0 or theta[0]<0 or theta[1]<-1 or theta[1]>1 or theta[2] <15000  or theta[3]<1 or theta[4]>theta[2] or (theta[2] * theta[3])< 100000):
        return([-10000])
    else:
        p_mu=theta[0]
        alpha=theta[1]
        time=int(theta[2])
        prod_rate=int(theta[3])
        rate_depo=int(theta[4])
        ## we fixed the number of time step and we look only at three parameter: posize copy and mutation
        exp=CCSimu(-1,time,pref,-1,p_mu,0,alpha,"file",dist_list=realdist,outputfile=False,mu_str=realsd,log=False,prod_rate=prod_rate,rate_depo=rate_depo)
        return exp.run()

data={'sd':allsds,'mean':allmeans}  

eps = ExponentialEps(100,1, 0.01)
prior = TophatPrior([0,-1,15000,10,100],[1,1,45000,80,10000])

pref=sys.argv[1] #a prefix that will be used as a folder to store the result of the ABC
mpi=bool(sys.argv[2])

### if use with MPI
if mpi : from  mpi_util import *

N=500
#
if mpi:
    mpi_pool = MpiPool()
    sampler = Sampler(N=N, Y=data, postfn=postfn, dist=dist,pool=mpi_pool) 
else:
    sampler = Sampler(N=N, Y=data, postfn=postfn, dist=dist)

sampler.particle_proposal_cls = OLCMParticleProposal

if mpi and mpi_pool.isMaster() and not os.path.exists(pref):
    os.makedirs(pref)
if not mpi and not os.path.exists(pref):
    os.makedirs(pref)

if mpi and mpi_pool.isMaster() :
    with open(pref+"/ratio.txt", "a") as myfile:
        myfile.write("T,epsilon,ratio\n")
elif not mpi:
    with open(pref+"/ratio.txt", "a") as myfile:
        myfile.write("T,epsilon,ratio\n")

for pool in sampler.sample(prior, eps):
    if mpi  and mpi_pool.isMaster() :
        with open(pref+"/ratio.txt", "a") as myfile:
            myfile.write(str(pool.t)+","+str(pool.eps)+","+str(pool.ratio)+"\n")
    if not mpi : 
        print("T:{0},eps:{1:>.4f},ratio:{2:>.4f}".format(pool.t, pool.eps, pool.ratio))
        for i, (mean, std) in enumerate(zip(np.mean(pool.thetas, axis=0), np.std(pool.thetas, axis=0))):
            print(u"    theta[{0}]: {1:>.4f},{2:>.4f}".format(i, mean,std))
    np.savetxt(pref+"/result_"+str(pool.eps)+".csv", pool.thetas, delimiter=",",header="p_mu,beta,time,prod_rate,rate_depo",fmt='%1.5f',comments="")

