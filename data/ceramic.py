import csv

realmeans= {"belen":171.181818181818,"delicias":172.084033613445,"malpica":166.054054054054,"parlamento":163.809523809524,"villaseca":160.207547169811}
samplesize= {"belen":88,"delicias":119,"malpica":111,"parlamento":42,"villaseca":53}

realsd={"exterior_diam":11,"protruding_rim":5, "rim_w":2.5, "rim_w_2":4}
realsd={"exterior_diam":.05,"protruding_rim":.05, "rim_w":.05, "rim_w_2":0.05}


def getrealdist():
    print("load workshop distiance using the file 'data/distmetrics.csv'")
    realdist={}
    with open('data/distmetrics.csv','rb') as distfile:
          distances = csv.reader(distfile, delimiter=',')
          for row in distances:
              realdist[row[0]+row[1]]=float(row[2]) #print(row)
              realdist[row[1]+row[0]]=float(row[2]) #print(row)
          #worldlist[distances[1]] = {distances[2],distances[3]}
    distfile.close()
    return(realdist)

#distances between workshops created by google maps
realdist=getrealdist() #a dictionnary storing the distance between all workshop in the form : "workshopAworkshopB"=> dist


