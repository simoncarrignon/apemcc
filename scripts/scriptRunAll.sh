#script to run expe 
time=30001
exp=$1
mkdir $exp
for m in "HT" "VT" "HTD";
do
	echo "Running simulation for model $m"
	mkdir "$exp"/"$m";
	for i in {1..200}; do 
        echo sim$i ; 
        python model/main.py -i file -w 5 -t $time -f "$exp"/"$m"/"$m"_"$i" -m "$m"; 
    done ; 
done
