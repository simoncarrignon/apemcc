#!/usr/bin/python

#A simple evolutionary model to study the evolution of workshop amphora production
#

import sys, getopt
import random 
import math

#Definition of the Agent which are workshop in our case:

class Workshop(object):
    dist=0
    id=""
    all_measures={}
    prod_rate=5

    #This function allow us to create a new workshop 
    def __init__(self, id, dist,all_measures,prod_rate):
        self.all_measures=all_measures
        self.id=id
        self.dist=dist
        print('New workshop called '+self.id+" at : "+str(self.dist)+" km")

    #fonction to use  str() in order to print a workshop as a string
    def __str__(self):
        return('Workshop '+self.id+" at distance: "+str(self.dist)+"\n\t they produce amphora with exterior_diam mean="+str(self.all_measures["exterior_diam"]["mean"])+", sd="+str(self.all_measures["exterior_diam"]["sd"]))
    
    #produce: show a production of amphora given the parameter of the function measure we use
    def produce(self,amount):
        for i in range(1,amount,1):
            amphsize= random.gauss(self.all_measures["exterior_diam"]["mean"],self.all_measures["exterior_diam"]["sd"])

    #writeProduce: write in a file the an amphora produced given the parameter of the workshop 
    def writeProduction(self,amount,t,res_file):
        for i in range(1,amount,1):
            amph=str(t)+","+self.id+","+str(self.dist)+",amphora_"+ str(i)
            for measure in self.all_measures:
                param=self.all_measures[measure]
                val=random.gauss(param["mean"],param["sd"])
                amph=amph+","+str(val)
            res_file.write(amph+"\n")


    #mutate: randomly change the parameter of production
    def mutate(self):
        up=-1
        if(random.randint(0,1)):up=1
        self.all_measures["exterior_diam"]["mean"] = self.all_measures["exterior_diam"]["mean"] + random.random()*10*up
        #self.all_measures["exterior_diam"]["sd"] = self.all_measures["exterior_diam"]["sd"] + random.random()*1-1

    def copy(self,ws2):
        up=-1
        if(random.randint(0,1)):up=1
        self.all_measures["exterior_diam"]["mean"] = ws2.all_measures["exterior_diam"]["mean"] #+ random.random()*2*up
        #self.all_measures["exterior_diam"]["sd"] = ws2.all_measures["exterior_diam"]["sd"] + random.random()*self.all_measures["exterior_diam"]["sd"]-self.all_measures["exterior_diam"]["sd"]

##Definition of the main function
def main(argv):

    #initialisation of the variable used during the simulation
    n_ws = 0   
    max_time = 0

###Folling lines using to parse the arguments from the command line
    try:
        opts, args = getopt.getopt(argv,"hw:t:",)
    except getopt.GetoptError:
        print 'apemcc.py -w <number of Workshop> -t <time>'
        sys.exit(2)
    if len(opts) < 1:
        print 'apemcc.py -w <number of Workshop> -t <time>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'apemcc.py -w <number of Workshop> -t <time>'
            sys.exit()
        elif opt == "-w":
           n_ws = int(arg)
        elif opt == "-t":
           max_time = int(arg)
#########################

    print str(n_ws), 'Workshop' 
    print 'During ', str(max_time), 'iterations' 

    world = list() #initialisation of the world


    production = open("result.csv", "w")
    header = "time,workshop,dist,amphora,exterior_diam\n"
    production.write(header)
    
    #forloop to create the wanted number of workshop an position them at equal distance
    for ws in range(0,n_ws,1):
        dist=ws**2
        #if(ws > 3):
        #    dist=ws+3
        #if ws > 6:
        #    dist=ws+9
        new_ws= Workshop('ws_'+str(ws),dist,{"exterior_diam":{"mean":160+ws,"sd":9}},10)
        world.append(new_ws)

##begin of the simulation
    for t in range(0,max_time,1):  
        for ws in world :
            if( t%1000 ==0): 
                ws.writeProduction(100,t,production)
                #print "timestep:", str(t)
            if( random.random()<.001):
                ws.mutate()
            n=random.randint(0,(n_ws-1))
            ws2 = world[n]
            if( ws.id != ws2.id and random.random() < .01):
                if(float(math.log(abs(ws.dist-ws2.dist)))/float(math.log((n_ws-1)**2)) < random.random() and ws.dist - ws2.dist <5):
                    #print(ws.dist,ws2.dist)
                    u=1
                    #print(float(abs(ws.dist-ws2.dist))/((n_ws)**3))
                    ws.copy(ws2)  


    production.close()



#
if __name__ == "__main__":
    main(sys.argv[1:])
