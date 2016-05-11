#!/usr/bin/python

#A simple evolutionary model to study the evolution of workshop amphora production
#

import sys, getopt
import random 

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
            amph=str(t)+","+self.id+";amphora_"+ str(i)
            for measure in self.all_measures:
                param=self.all_measures[measure]
                val=random.gauss(param["mean"],param["sd"])
                amph=amph+","+str(val)
            res_file.write(amph+"\n")


    #mutate: randomly change the parameter of production
    def mutate(self):
        self.all_measures["exterior_diam"]["mean"] = self.all_measures["exterior_diam"]["mean"] + random.random()*2-2
        self.all_measures["exterior_diam"]["sd"] = self.all_measures["exterior_diam"]["sd"] + random.random()*1-1

    def copy(self,ws2):
        self.all_measures["exterior_diam"]["mean"] = ws2.all_measures["exterior_diam"]["mean"] + random.random()*self.all_measures["exterior_diam"]["sd"]-self.all_measures["exterior_diam"]["sd"]
        self.all_measures["exterior_diam"]["sd"] = ws2.all_measures["exterior_diam"]["sd"] + random.random()*self.all_measures["exterior_diam"]["sd"]-self.all_measures["exterior_diam"]["sd"]

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


    production = open("result.csv", "rw+")
    header = "time,workshop,exterior_diam\n"
    production.write(header)
    
    #forwe create the wanted number of workshop an position them at equal distance
    for ws in range(1,n_ws,1):
        new_ws= Workshop('ws_'+str(ws),ws,{"exterior_diam":{"mean":160,"sd":9}},10)
        world.append(new_ws)

##begin of the simulation
    for t in range(0,max_time,1):  
        print "timestep:", str(t)
        for ws in world :
            ws.writeProduction(10,t,production)
            if( random.random()<.01):
                ws.mutate()
                for ws2 in world :
                    if (abs(ws.dist-ws2.dist)/n_ws):
                        ws.copy(ws2) #Horizontal transfer


    production.close()



#
if __name__ == "__main__":
    main(sys.argv[1:])
