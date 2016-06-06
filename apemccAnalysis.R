
if(require("vioplot")){library(vioplot)}
if(require("vegan")){library(vegan)}

analyseModel<-function(){
model=read.csv("result.csv") ;  
model=model[!is.na(model)]
model=model[model$time >= max(model$time)-1000,]; 
cubeCC=cubeC[cubeC$time >= max(cubeC$time)-1000,]; 
model=model[order(model$dist),];



png("CYDS.png")
boxplot(model$exterior_diam ~ model$dist,ylab="exterior_rim",xlab="workshop",xaxt="n")
axis(1,labels=levels(model$workshop),at=1:length(unique(model$dist)))
dev.off()

png("CNDS.png")
boxplot(model$exterior_diam ~ model$dist,ylab="exterior_rim",xlab="workshop",xaxt="n")
axis(1,labels=levels(model$workshop),at=1:length(unique(model$dist)))
dev.off()

png("CYDL.png")
boxplot(model$exterior_diam ~ model$dist,ylab="exterior_rim",xlab="workshop",xaxt="n")

axis(1,labels=levels(model$workshop),at=1:length(unique(model$dist)))
dev.off()

png("CNDL.png")
boxplot(model$exterior_diam ~ model$dist,ylab="exterior_rim",xlab="workshop",xaxt="n")
axis(1,labels=levels(model$workshop),at=1:length(unique(model$dist)))
dev.off()

plot

}

analyseRealData<-function(){

emp=read.csv("data/dres.csv")
	boxplot(emp$protruding_rim ~ emp$site)
	cov(emp$rim_h,emp$rim_w)
	cor(emp$rim_h,emp$rim_w)
	cov(emp$exterior_diam,emp$rim_w)
	cor(emp$exterior_diam,emp$rim_h)
	plot(emp$exterior_diam~emp$inside_diam)
	cov(emp$exterior_diam,emp$inside_diam)
	abline(
	       lm(emp$exterior_diam~emp$rim_w)
	       )
	mean(tapply(emp$exterior_diam,emp$site,mean))
	tapply(emp$exterior_diam,emp$site,length)
	sd(emp$exterior_diam)
	sd(tapply(cubeC$exterior_diam,cubeC$workshop,mean))
	sd(cubeC$exterior_diam)
	mean(tapply(model$exterior_diam,model$workshop,sd))
	sd(model$exterior_diam)

vioplot2(emp,"site","protruding_rim")
vioplot2(cubeC,"workshop","exterior_diam")

pdf("prot.pdf")
vioplot2(emp,"site","protruding_rim",main="Size of the protruding rim in each workshop")
dev.off()

defN4=read.csv("default_N4.csv")
vioplot2(defN4,"workshop","exterior_diam")

defN4=read.csv("lineC/lineC_100_N4.csv")
vioplot2(getLastIt(defN4),"workshop","exterior_diam")
	sd(tapply(emp$exterior_diam,emp$site,mean))

tsd=c()
for(i in unique(defN4$time)){
	tsd=c(tsd,sd(tapply(defN4$exterior_diam[defN4$time==i],defN4$workshop[defN4$time==i],mean)))
}
plot(tsd)

	tapply(defN4$exterior_diam,defN4$workshop,sd)
aa=varWorkshopTime(defN4)
varOfVar=t(varSim(cubeC))
timesel=seq(0,8000,2000)
allExpeb=list(t(varSim(lineC[lineC$time %in% timesel ,])),
	 t(varSim(lineNC[lineNC$time %in% timesel ,])),
	 t(varSim(cubeC[cubeC$time %in% timesel ,])),
	 t(varSim(cubeNC[cubeNC$time %in% timesel ,]))
	 )
png("lineC.png")
vioplot3(t(varSim(limitTimeStep(lineC,timesel) )),ylim=c(0,30),main="Evolution of interworkshop variance",ylab="Var in Exterior Diam. Mean. Size",xlab="Time")
dev.off()
png("lineNC.png")
vioplot3(t(varSim(limitTimeStep(lineNC,timesel) )),ylim=c(0,30),main="Evolution of interworkshop variance",ylab="Var in Exterior Diam. Mean. Size",xlab="Time")
dev.off()
png("cubeC.png")
vioplot3(t(varSim(limitTimeStep(cubeC,timesel) )),ylim=c(0,30),main="Evolution of interworkshop variance",ylab="Var in Exterior Diam. Mean. Size",xlab="Time")
dev.off()
png("cubeNC.png")
vioplot3(t(varSim(limitTimeStep(cubeNC,timesel) )),ylim=c(0,30),main="Evolution of interworkshop variance",ylab="Var in Exterior Diam. Mean. Size",xlab="Time")
dev.off()
boxplot(t(varSim(cubeNC)))
boxplot(t(varSim(lineC)))
boxplot(t(varSim(lineNC)))
cubeC=readFolder("cubeC/")
vioplot2(cubeC,"workshop","exterior_diam")


##LAST GRAPH
juntos=c()
juntos=rbind(
	     varSim(getLastIt(lineNC)),
	     varSim(getLastIt(cubeC)),
	     varSim(getLastIt(lineC))
	     )
rownames(juntos)=c("","","")#expression(frac(1,d^3)),"1/d")
pdf("interworkshopvar.pdf",pointsize=20)
vioplot3(t(juntos),ylim=c(0,40),ylab="Interworkshops variation (cm)",xlab="P(T)",xaxt="n")
axis(1,label=c("0",expression(1%/%d^3),expression(1%/%d)),at=1:3)
dev.off()
#axis(1,label=c("0",expression(frac(1,d^3)),expression(frac(1,d))),at=1:3)

colnames(u)[ncol(u)]="PA"
juntos=rbind(juntos,u)
u=cbind(getLastIt(lineC),"lineC")
colnames(u)[ncol(u)]="PA"
juntos=rbind(juntos,u)
u=cbind(getLastIt(cubeC),"cubeC")
colnames(u)[ncol(u)]="PA"
juntos=rbind(juntos,u)
	     
vioplot2(juntos,"PA","exterior_diam")

cubeC10=readFolder("cubeC10/")
vioplot2(cubeC10,"workshop","exterior_diam")

cubeNC=readFolder("cubeNC/")
vioplot2(cubeNC,"workshop","exterior_diam")

lineC=readFolder("lineC/")
vioplot2(lineC,"workshop","exterior_diam")

lineNC=readFolder("lineNC/")
vioplot2(getLastIt(cubeNC),"workshop","exterior_diam")

pn3C=readFolder("pn3/")
vioplot3(t(varSim(limitTimeStep(pn3C,timesel) )),ylim=c(0,30),main="Evolution of interworkshop variance",ylab="Var in Exterior Diam. Mean. Size",xlab="Time")

	sd(lineNC$exterior_diam)
	sd(cubeC$exterior_diam)
	sd(getLastIt(lineC)$exterior_diam)
	sd(getLastIt(lineNC)$exterior_diam)

	diversity(getLastIt(cubeC)$exterior_diam)
	diversity(getLastIt(cubeNC)$exterior_diam)
	diversity(getLastIt(lineC)$exterior_diam)
	diversity(getLastIt(lineNC)$exterior_diam)
	diversity(emp$exterior_diam)
}


vioplot2<-function(data,x,y,...){
    levx=levels(data[,x])
    xmax=length(levx)
    
    ymax=max(data[,y])
    ymin=min(data[,y])
    plot(1,1,xlim=c(0.5,xmax+.5),ylim=c(ymin,ymax),type="n",xaxt="n",ylab="Size",xlab="",...)
    axis(1,at=1:xmax,labels=levx)
    sapply(1:xmax,function(k){
	   tmp=data[data[,x] == levx[k] , y ]
	   vioplot(tmp,at=k,add=T,col="white")
	       })
}

vioplot3<-function(data,...){
    levx=colnames(data)
    xmax=length(levx)
    
    ymax=max(data)
    ymin=min(data)
#ylim=c(ymin,ymax),
    plot(1,1,xlim=c(0.5,xmax+.5),type="n",xaxt="n",...)
    axis(1,at=1:xmax,labels=levx)
    sapply(1:xmax,function(k){
	   tmp=data[ , k ]
	   vioplot(tmp,at=k,add=T,col="white")
	       })
   
}
#take list of truc and amkle truc
vioplot4<-function(data,...){
    levx=colnames(data[[1]])
    xmax=length(levx)
    
    ymax=max(sapply(data,max))
    ymin=min(sapply(data,min))
    plot(1,1,xlim=c(0.5,xmax+.5),ylim=c(ymin,ymax),type="n",xaxt="n",...)
    axis(1,at=1:xmax,labels=levx)
    for(i in 1:length(data)){
	tmp=data[[i]]
	sapply(1:xmax,function(k){
	       print(paste(i,k))
	       vioplot(tmp[ , k ],at=(k+.65)-(i/4),add=T,wex=.2,col=i)
	       })
    }
   
}


readFolder<-function(fname){
    res=c()
    id=0
    for(i in list.files(fname,pattern= "*.csv",full.names=T)){
	   print(i)
	res=rbind(res,cbind(read.csv(i),id))
	id=id+1
    }
    return(res)
}

getLastIt<-function(data){
    return(data[data$time >= max(data$time),])
}

varWorkshopTime<-function(data){
    sapply(unique(data$time),function(i){
		     r=sd(tapply(data$exterior_diam[data$time==i],data$workshop[data$time==i],mean))
		     names(r)=i
		     return(r)
    })
}

varSim<-function(data){
	sapply(unique(data$id),function(i){
	       tmp=data[data$id == i,]
	       varWorkshopTime(tmp)
    })
}

limitTimeStep<-function(data,timelist){
return(data[data$time %in% timelist ,])
}
