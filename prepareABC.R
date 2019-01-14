source("../../../full_projects/icrates_abc/scripts/ext_scripts/abctools.R")

emp <- getRealMeasurment()
write.csv(file="mean_sd_bySite.csv",rbind(mean = tapply(emp$exterior_diam,emp$site, mean),sd =tapply(emp$exterior_diam,emp$site, sd)))

generalModel=rnorm(100,mean(emp$exterior_diam),sd(emp$exterior_diam))
samplemodel=generalModel[sample.int(53)]

sd(generalModel)
sd(samplemodel)
mean(generalModel)
mean(samplemodel)

allmeasurment=emp[,5:12]

globalmeaneachmeasurmen=apply(allmeasurment,2,mean)

globalsdeachmeasurmen=apply(allmeasurment,2,sd)

samplesizepersite=tapply(emp$exterior_diam,emp$site, length)
allmeasurment.sd = sapply(5:12,function(i)tapply(emp[,i],emp$site, sd))
allmeasurment.mean = sapply(5:12,function(i)tapply(emp[,i],emp$site, mean))

colnames(allmeasurment.mean)=colnames(emp)[5:12]
colnames(allmeasurment.sd)=colnames(emp)[5:12]
write.csv(file="mean_allmeasurment.csv",allmeasurment.mean)
write.csv(file="mean_allmeasurment.csv",allmeasurment.mean)
