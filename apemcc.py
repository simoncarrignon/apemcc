#!/usr/bin/python

#A simple evolutionary model to study the evolution of workshop amphora production
#

import sys, getopt
import random 
import math
import csv

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

    #fonction to use  str() in order to print a workshop as a string (in this case doesnt work with this code)
    #def __str__(self):
        #return('Workshop '+self.id+" at distance: "+str(self.dist)+"\n\t they produce amphora with exterior_diam mean="+str(self.all_measures["exterior_diam"]["mean"])+", sd="+str(self.all_measures["exterior_diam"]["sd"]))
    
    #produce: show a production of amphora given the parameter of the function measure we use (in this case doesnt work with this code)
    #def produce(self,amount):
        #for i in range(1,amount,1):
            #amphsize= random.gauss(self.all_measures["exterior_diam"]["mean"],self.all_measures["exterior_diam"]["sd"])

    #writeProduce: write in a file the amphora produced given the parameter of the workshop 
    #if amount>0 it will limit the number of amphora written in the output file (
    def writeProduction(self,t,res_file,amount=0):
        if amount == 0:
            amount=self.prod_rate

        for i in range(1,amount,1):
            amph=str(t)+","+self.id+","+str(self.dist)+",amphora_"+ str(i)
            for measure in self.all_measures:
                param=self.all_measures[measure]
                val=random.gauss(param["mean"],param["sd"])
                amph=amph+","+str(val)
            res_file.write(amph+"\n")


    #mutate: randomly change the parameter of production
    def mutate(self):
        for measure in self.all_measures:
            up=-1 #increase or decrease the value
            if(random.randint(0,1)):up=1 #randomly  increase or decrease the size
            self.all_measures[measure]["mean"] = self.all_measures[measure]["mean"] + random.random()*10*up

    def copy(self,ws2):
        for measure in self.all_measures:
            up=-1
            if(random.randint(0,1)):up=1
            self.all_measures[measure]["mean"] = ws2.all_measures[measure]["mean"] #+ random.random()*2*up
            #self.all_measures["exterior_diam"]["sd"] = ws2.all_measures["exterior_diam"]["sd"] + random.random()*self.all_measures["exterior_diam"]["sd"]-self.all_measures["exterior_diam"]["sd"]

    #def dist(self,ws2):
    #    return(mat_dist[self.id,ws2.id])
    ##self.all_measures["exterior_diam"]["sd"] = ws2.all_measures["exterior_diam"]["sd"] + random.random()*self.all_measures["exterior_diam"]["sd"]-self.all_measures["exterior_diam"]["sd"]
#########################
#########################
#########################
#########################

##Definition of the main function
def main(argv):

    #initialisation of the variable used during the simulation
    n_ws = 0   
    max_time = 0
    outfile = "default"

###Folling lines using to parse the arguments from the command line
    use='apemcc.py -w <number of Workshop> -t <time> -f <file> -m <model>\n model should be in {"HT","HTD","VT"}'

    try:
        opts, args = getopt.getopt(argv,"hw:t:f:m:",)
    except getopt.GetoptError:
        print use
        sys.exit(2)
    if len(opts) < 1:
        print use
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print use
            sys.exit()
        elif opt == "-w":
           n_ws = int(arg)
        elif opt == "-t":
           max_time = int(arg)
        elif opt == "-f":
           outfile = str(arg)
        elif opt == "-m":
           model = str(arg)
#########################
##TODO: allow to easily switch from workshop in a file vs workshop created onthefly

    print str(n_ws), 'Workshop' 
    print 'During ', str(max_time), 'iterations' 

    world = list() #initialisation of the world
    world_dist=dict() #dictionnaire to store the distance of the cities two by two

    with open('data/distmetrics.csv','rb') as distfile:
          distances = csv.reader(distfile, delimiter=',')
          for row in distances:
              world_dist[row[0]+row[1]]=float(row[2]) #print(row)
              world_dist[row[1]+row[0]]=float(row[2]) #print(row)
          #worldlist[distances[1]] = {distances[2],distances[3]}


    outfilename=outfile+"_"+"N"+str(n_ws)+".csv"
    prodfile = open(outfilename, "w")
    header = "time,workshop,dist,amphora,exterior_diam,protruding_rim,rim_w,rim_w_2\n"
    prodfile.write(header)
    pn=5
    
    #forloop to create the wanted number of workshop an position them at equal distance
    #Should be used only in the theoretical case (as presented in Birmingham 2016)

    #for ws in range(0,n_ws,1):
    #    dist=ws
    #    #if(ws > 3):
    #    #    dist=ws+3
    #    #if ws > 6:
    #    #    dist=ws+9
    #    new_ws= Workshop('ws_'+str(ws),dist,{"exterior_diam":{"mean":167.7+ws,"sd":12.26},"protruding_rim":{"mean":19+ws,"sd":5.6}},10)
    #    world.append(new_ws)


    for ws in  {"villaseca","belen","malpica","delicias","parlamento"}:
        dist=10 #this is not use in that case as the "distance" are given by the dictionnary world_dict
        new_ws= Workshop(ws,dist,{"exterior_diam":{"mean":167.7,"sd":12.26},"protruding_rim":{"mean":19,"sd":5.6}, "rim_w":{"mean":36.29,"sd": 4.76}, "rim_w_2":{"mean": 30.35,"sd": 5.38}},100)
        world.append(new_ws)

##begin of the simulation
    print "starting the simulation with copy mechanism:",model
    for t in range(0,max_time,1):  
        for ws in world :
            if( t%1000 ==0): 
                ws.writeProduction(t,prodfile)
                #print "timestep:", str(t)
            if( random.random()<.001):
                ws.mutate()
            n=random.randint(0,(n_ws-1))
            ws2 = world[n]
            if( ws.id != ws2.id and random.random() < .01):  #with a 1/100 proba we initialize a copy
                rel_dist=world_dist[ws2.id+ws.id] #get the distance between two given workshop
                r=random.random()
                if(  model == "HT"):
                    proba= 1   #no effect of distance between the workshop ie everybody copy everybody with same proba of 1/100
                elif model== "HTD":
                    proba=(float(rel_dist)-(8.13))/((95.33)-(8.13)) < random.random() #should be true when two workshop are close to eachother
                elif model == "VT": 
                    proba= 0
                print proba

                if proba:
                    ws.copy(ws2)  

    prodfile.close()
    print "simulation done."




#
if __name__ == "__main__":
    main(sys.argv[1:])
