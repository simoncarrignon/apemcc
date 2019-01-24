from sampler import *
from threshold import *
import numpy as np
import sys,os

from model.apemcc import CCSimu
from data.ceramic import *



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
        allm=x[w].production["protruding_rim"]
        realsummary=data['mean'][w]["protruding_rim"]
        realsummary=np.mean(allm[len(allm)-(10*1000):])
        alldist.append(abs(realsummary-np.mean(allm)))
    return np.mean(alldist)

#our "model", a gaussian with varying means
def postfn(theta):
    # we reject the particul with no credible parameters (ie pop < 0 etc...)
    #if(theta[0]>1 or theta[1]<0 or theta[1]>1 or theta[0]<0):
    if(theta[1]>1 or theta[1]<0 or theta[2]<-1 or theta[2]>1):
        return([-10000])
    else:
        time=30000
        p_mu=theta[1]
        alpha=theta[2]
        ## we fixed the number of time step and we look only at three parameter: posize copy and mutation
        exp=CCSimu(-1,time,pref,-1,p_mu,0,alpha,"file",dist_list=realdist,outputfile=False,mu_str=realsd,log=False)
        return exp.run()

data={'sd':allsds,'mean':allmeans}  #we dont use it in this expe

eps = ExponentialEps(200,25, 0.01)
prior = TophatPrior([1000,0,-1],[30000,0.01,1])

pref=sys.argv[1] #a prefix that will be used as a folder to store the result of the ABC
mpi=bool(sys.argv[2])

### if use with MPI
if mpi : from  mpi_util import *

#
if mpi:
    mpi_pool = MpiPool()
    sampler = Sampler(N=200, Y=data, postfn=postfn, dist=dist,pool=mpi_pool) 
else:
    sampler = Sampler(N=200, Y=data, postfn=postfn, dist=dist)

if mpi and mpi_pool.isMaster() and not os.path.exists(pref):
    os.makedirs(pref)
elif not os.path.exists(pref):
    os.makedirs(pref)

for pool in sampler.sample(prior, eps):
    if mpi and mpi_pool.isMaster():
        logFile = open(pref+'/general.txt', 'a')
        logFile.write('starting eps: '+str(pool.eps)+'\n')
        logFile.close()
        np.savetxt(pref+"/result_"+str(pool.eps)+".csv", pool.thetas, delimiter=",",fmt='%1.5f',comments="")
        with open(pref+"/ratio.txt", "a") as myfile:
            myfile.write(str(pool.t)+","+str(pool.eps)+","+str(pool.ratio)+"\n")
    else: 
        print("T:{0},eps:{1:>.4f},ratio:{2:>.4f}".format(pool.t, pool.eps, pool.ratio))
        for i, (mean, std) in enumerate(zip(np.mean(pool.thetas, axis=0), np.std(pool.thetas, axis=0))):
            print(u"    theta[{0}]: {1:>.4f},{2:>.4f}".format(i, mean,std))
    #np.savetxt(bias+"/result_"+str(pool.eps)+".csv", pool.thetas, delimiter=",",header="n_agents,time,p_mu,p_copy",fmt='%1.5f',comments="")
        np.savetxt(pref+"/result_"+str(pool.eps)+".csv", pool.thetas, delimiter=",",fmt='%1.5f',comments="")

