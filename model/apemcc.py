#!/usr/bin/python

#A simple evolutionary model to study the evolution of workshop amphora production
#

import random 
import math
import csv
from Workshop import Workshop #import the agent class

#distances between workshops created by google maps
#"parlamento","belen",72.45
#"parlamento","delicias",82.01
#"parlamento","malpica",74.77
#"belen","parlamento",72.45
#"belen","delicias",22.82
#"belen","malpica ",8.73
#"delicias","parlamento",82.01
#"delicias","belen",22.82
#"delicias","malpica",14.19
#"malpica","parlamento",74.77
#"malpica","belen",8.73
#"malpica","delicias",14.19
#"villaseca","belen",25.23
#"villaseca","malpica",20.97
#"villaseca","delicias",22.45
#"villaseca","parlamento",95.33

#Definition of the Agent which are workshop in our case:
class CCSimu(object):
    n_ws=-1 ##if no number of workshop given we us 5
    max_time= 10000
    outfile= "output"
    model= "VT"

    #Some usual default parameters:
    #p_mu=.001 ##mutation probability 1 other 1000 .1 percent
    #p_copy=.01 ##probability of copy
    #d_weight=1 #weight of the distance 

    p_mu=.001
    p_copy=.01
    d_weight=1
    world=list()
    world_list=dict()
    world_lim=list()
    prodfile=""
    init=""
    rate_depo=1000 #the rate at wish workshop will write their deposit in the outputfile

    def __init__(self,n_ws,max_time,pref,model,p_mu,p_copy,d_weight,init):
        self.n_ws=n_ws
        self.max_time=max_time
        self.pref=pref #us eto classify differetn type of simulation
        self.model=model
        self.p_mu=p_mu
        self.p_copy=p_copy
        self.d_weight=d_weight
        self.init=init

        print 'Initialization of the world' 
        print str(self.n_ws), 'Workshop' 
        print 'During ', str(self.max_time), 'iterations' 

        self.world = list() #initialisation of the world
        self.world_dist=dict() #dictionnaire to store the distance of the cities two by two

        pn=5

        self.world_lim={"exterior_diam":{"min":130,"max":200},"protruding_rim":{"min":5,"max":40}, "rim_w":{"min":25,"max": 48}, "rim_w_2":{"min": 15,"max": 44}}
        if self.init=="file":
            print("initialize the workshop using the file 'data/distmetrics.csv'")
            print("warning:argument"+" number of workshop"+" will be ignored")
            with open('data/distmetrics.csv','rb') as distfile:
                  distances = csv.reader(distfile, delimiter=',')
                  for row in distances:
                      self.world_dist[row[0]+row[1]]=float(row[2]) #print(row)
                      self.world_dist[row[1]+row[0]]=float(row[2]) #print(row)
                  #worldlist[distances[1]] = {distances[2],distances[3]}


                  #(1) mean of mean btw ws (2)sd of mean btw ws (3)min (4)max
                  #measurement:             (1)                 (2)     (3) (4)
                  #exterior_diam           166.667395         4.9998310 130 200
                  #inside_diam              93.631245         1.3069177  70 140
                  #rim_h                    35.387083         0.8810068  25  48
                  #rim_w                    36.686752         1.9171952  25  48
                  #shape_w                   9.646956         0.6530906   5  14
                  #rim_inside_h             28.373472         1.1329995  20  39
                  #rim_w_2                  31.054947         1.2328019  15  44
                  #protruding_rim           18.273888         3.2735080   5  40
                 #exteri    or_diam    inside_diam          rim_h          rim_w        shape_w  rim_inside_h        rim_w_2 protruding_rim
                 #     1    1.126504       9.250002       3.004174       3.494843       1.080722       2.976005       4.216725       4.790658
            #the mean standard deviation for every measurment
            self.maxdist=max(self.world_dist.values())
            self.mindist=min(self.world_dist.values())
             
            for ws in  {"villaseca","belen","malpica","delicias","parlamento"}:
                dist=10 #this is not use in that case as the "distance" are given by the dictionnary world_dict
                new_ws= Workshop(ws,dist,{"exterior_diam":{"mean":167.90,"sd":11},"protruding_rim":{"mean":18.30,"sd":5}, "rim_w":{"mean":37.23,"sd": 2.5}, "rim_w_2":{"mean": 31.24,"sd": 4}},100,self.world_lim)
                self.world.append(new_ws)
            self.n_ws=len(self.world)

        elif self.init=="art":
            print("initialize"+str(self.n_ws)+" workshop randomly")
            for ws in range(self.n_ws):
                dist=ws
                #if(ws > 3):
                #    dist=ws+3
                #if ws > 6:
                #    dist=ws+9
                new_ws= Workshop('ws_'+str(ws),dist,{"exterior_diam":{"mean":167.7+ws,"sd":12.26},"protruding_rim":{"mean":19+ws,"sd":5.6}},10,self.world_lim)
                self.world.append(new_ws)

        outfilename=self.pref+"_"+"N"+str(self.n_ws)+".csv"
        self.prodfile = open(outfilename, "w")
        header = "time,workshop,dist,amphora,exterior_diam,protruding_rim,rim_w,rim_w_2\n"
        self.prodfile.write(header)

    def getrelativedist(self,dis):
        return((float(dis)-(self.mindist))/((self.maxdist)-(self.mindist)))


    def run(self): ##main function of the class Experiment => run a simulation

        relative=True
##begining of the simulation
        print("starting the simulation with copy mechanism: "+str(self.model))
        for t in range(0,self.max_time,1):  
            for ws in self.world :
                if( t%self.rate_depo ==0): 
                    ws.writeProduction(t,self.prodfile)
                if( random.random()< self.p_mu):
                    ws.mutate()
                n=random.randint(0,(self.n_ws-1))
                ws2 = self.world[n]
                if( ws.id != ws2.id and random.random() < self.p_copy):  #with a 1/100 proba we initialize a copy
                    if(self.init=="file"):
                        dist=self.world_dist[ws2.id+ws.id] #get the distance between two given workshop
                        if(relative):
                            dist=self.getrelativedist(dist)
                    elif self.init == "art":
                        dist=ws2.dist-ws.dist
                    r=random.random()
                    if(  self.model == "HT"):
                        proba= 1   #no effect of distance between the workshop ie everybody copy everybody with same proba of 1/100
                    elif self.model== "HTD":
                        proba= dist < random.random()*self.d_weight  #should be true when two workshop are close to eachother
                    elif self.model == "VT": 
                        proba= 0

                    if proba:
                        ws.copy(ws2)  
        print "simulation done."



