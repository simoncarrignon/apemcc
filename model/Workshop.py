import random 

#Definition of the Agent which are workshop in our case:
class Workshop(object):
    dist=0
    id=""
    all_measures={}
    prod_rate=-1
    mutation_power=.05
    world_lim={}

    #This function allow us to create a new workshop 
    def __init__(self, id, dist,all_measures,prod_rate,world_lim):
        self.all_measures=all_measures
        self.world_lim=world_lim
        self.id=id
        self.prod_rate=prod_rate
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
            self.all_measures[measure]["mean"] = self.all_measures[measure]["mean"] + self.all_measures[measure]["mean"]* self.mutation_power  *up
            while self.all_measures[measure]["mean"] > (self.world_lim[measure]["max"]*1.1) or self.all_measures[measure]["mean"] < (self.world_lim[measure]["min"]*.9):
                if self.all_measures[measure]["mean"] > (self.world_lim[measure]["max"]*1.1):
                    up=-1
                else :
                    up = 1 
                self.all_measures[measure]["mean"] = self.all_measures[measure]["mean"] + self.all_measures[measure]["mean"]* self.mutation_power  *up
            #self.all_measures[measure]["sd"] = self.all_measures[measure]["sd"]+  self.all_measures[measure]["sd"]*self.mutation_power*.01 *up # + random.random()*self.all_measures["exterior_diam"]["sd"]-self.all_measures["exterior_diam"]["sd"]

    def copy(self,ws2):
        for measure in self.all_measures:
            up=-1
            if(random.randint(0,1)):up=1
            self.all_measures[measure]["mean"] = ws2.all_measures[measure]["mean"] #+  self.all_measures[measure]["mean"]*self.mutation_power  *up
            self.all_measures[measure]["sd"] = ws2.all_measures[measure]["sd"]
            #while self.all_measures[measure]["mean"] > self.world_lim[measure]["max"] or self.all_measures[measure]["mean"] < self.world_lim[measure]["min"]:
            #    if self.all_measures[measure]["mean"] > self.world_lim[measure]["max"]:
            #        up=-1
            #    else :
            #        up = 1 
            #    self.all_measures[measure]["mean"] = self.all_measures[measure]["mean"] + self.all_measures[measure]["mean"]* self.mutation_power  *up
            #self.all_measures[measure]["sd"] = ws2.all_measures[measure]["sd"]+  self.all_measures[measure]["sd"]*.0001 *up # + random.random()*self.all_measures["exterior_diam"]["sd"]-self.all_measures["exterior_diam"]["sd"]

    #def dist(self,ws2):
    #    return(mat_dist[self.id,ws2.id])
    ##self.all_measures["exterior_diam"]["sd"] = ws2.all_measures["exterior_diam"]["sd"] + random.random()*self.all_measures["exterior_diam"]["sd"]-self.all_measures["exterior_diam"]["sd"]
#########################
#########################
#########################
#########################


