# apemcc
Amphora Production, an Evolutionary model of culture change

### usage :

```bash
python model/main.py -w <number of Workshop> -t <time> -f <outputfile> -m <model> -i <init>
```

* `time` is the total number of time step of the simulation 
* `init` should be in `{"art","file"}`
* `model` should be in `{"HT","HTD","VT"}`
* `outputfile` wille be use to write and store the results of the model

If `-i file` is used `-w` is not use

to run lot of script:

```bash
bash scripts/scriptRunAll.sh
```
