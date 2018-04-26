import sys, getopt
from apemcc import CCSimu

if __name__ == "__main__":
    argv=sys.argv[1:]

    #initialisation of the variable used during the simulation
    ntws = 0   
    max_time = 0
    outfile = "default"

###Folling lines using to parse the arguments from the command line
    use='apemcc.py -w <number of Workshop> -t <time> -f <outputfile> -m <model> -i <init>\n `time` is the total number of time step of the simulation \n `init` should be in {"art","file"}\n `model` should be in {"HT","HTD","VT"}\n `outputfile` wille be use to write and store the results of the model'

    try:
        opts, args = getopt.getopt(argv,"hw:t:f:m:i:",)
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
        elif opt == "-i":
           init = str(arg)
           
    p_mu=.001 ##mutation probability 1 other 1000 .1 percent
    p_copy=.01 ##probability of copy
    d_weight=.7 #weight of the distance

    main_exp=CCSimu(n_ws,max_time,outfile,model,p_mu,p_copy,d_weight,init)

    main_exp.run()

