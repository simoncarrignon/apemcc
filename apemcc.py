#!/usr/bin/python

#A simple evolutionary model to study the evolution of workshop amphora production
#

import sys, getopt

def main(argv):
    n_ws = 0
    t = 0
    try:
        opts, args = getopt.getopt(argv,"hw:t:",)
    except getopt.GetoptError:
        print 'apemcc.py -w <number of Workshop> -t <time>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'apemcc.py -w <number of Workshop> -t <time>'
            sys.exit()
        elif opt == "-w":
           n_ws = arg
        elif opt == "-t":
           max_time = arg
    print n_ws, 'Workshop' 
    print 'During ', t, 'iterations' 



if __name__ == "__main__":
    main(sys.argv[1:])
