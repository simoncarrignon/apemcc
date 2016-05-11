#!/usr/bin/python

#A simple evolutionary model to study the evolution of workshop amphora production
#

import sys, getopt

#Definition of the Agent which are workshop in our case:

class Workshop(object):
    dist=0
    id=""
    def __init__(self, id, dist):
        self.dist=dist
        self.id=id
        print('New workshop called '+self.id+" at : "+str(self.dist)+" km")

    def __str__(self):
        return('Workshop '+self.id+" at distance: "+str(self.dist))


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

    #forwe create the wanted number of workshop an position them at equal distance
    for ws in range(1,n_ws,1):
        new_ws= Workshop('ws_'+str(ws),ws)
        world.append(new_ws)

##begin of the simulation
    for t in range(0,max_time,1):
        print "timestep:", str(t)
        for ws in world :
            print(ws)





#
if __name__ == "__main__":
    main(sys.argv[1:])
