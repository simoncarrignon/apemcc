#script to run expe 
time=30001
exp=$1
mkdir $exp
cd $exp
for m in "HT" "VT" "HTD";
do
	echo "Running simulation for model $m"
	mkdir $m;
	for i in {1..100}; do echo sim$i ; ./apemcc.py -w 5 -t $time -f "$m"/"$m"_"$i" -m "$m" >> $m/log_"$m" ; done ; 
done
cd ..
