# apemcc
Amphora Production, an Evolutionary model of culture change


## Basic  Usage:
If you want to run just one simulation you need to use `main.py` and give to this script the good argument:

### run

```bash
python model/main.py -w <number of Workshop> -t <time> -f <outputfile> -m <model> -i <init> -a <alpha>
```

* `time` is the total number of time step of the simulation 
* `init` should be in `{"art","file"}`
* `model` should be in `{"HT","HTD","VT"}`
* `outputfile` wille be use to write and store the results of the model
* `alha` new gradual bias (-1 = HT, .5 = HTD, 1 = VT)

If `-i file` is used `-w` is not use

### analyse
If you use let say:

```bash
python main.py -w 10 -t 10000 -f singletest -m HT -i "art" -a 10
```

the model will create a file: `singletest_N10.csv` and you can analyse it with R and some of the tools available in 
* `scripts/apemccAnalysis.R`  
* `scripts/testBetaFunction.R`  

For exemple to see how the exterior rim change between workshops:
```R
model=read.csv("../singletest_N10.csv")  
boxplot(model$exterior_diam ~ model$dist,ylab="exterior_rim",xlab="workshop",xaxt="n")
axis(1,labels=levels(model$workshop),at=1:length(unique(model$dist)))
```

Or how the size of exterior rim change through time within the workshop 1:

```R
boxplot(model$exterior_diam[model$workshop == "ws_1"] ~ model$time[model$workshop == "ws_1"],ylab="exterior_rim",xlab="time"")
```


## Simple experiments with Thresholded bias :

As an intermediate way between the single simulation and a full ABC using MPI you can play with the script used to generate the result use for the first versions of the exploration of the model

```bash
bash scripts/scriptRunAll.sh folder
```

where `folder` is the path to a folder where the results of the experiment will be stored

It should be noted that this is a modification done in order to simulate the first bias with the new `alpha` parameter

## Simple experiments with Thresholded bias :
