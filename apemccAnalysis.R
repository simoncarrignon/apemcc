
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

emp=read.csv("data/drespaper.csv")
emp=emp[ emp$type != "Dressel 23",]
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
	tapply(emp$exterior_diam,emp$site,mean)
	sd(emp$exterior_diam)
	sd(tapply(cubeC$exterior_diam,cubeC$workshop,mean))
	sd(cubeC$exterior_diam)
	mean(tapply(model$exterior_diam,model$workshop,sd))
	sd(model$exterior_diam)

	apply(emp[,5:12],2,sd)/	apply(emp[,5:12],2,mean)
	summary=rbind(apply(emp[,5:12],2,sd),	apply(emp[,5:12],2,mean))

vioplot2(emp,"site","protruding_rim")
vioplot2(cubeC,"workshop","exterior_diam")

pdf("prot.pdf")
vioplot2(emp,"site","protruding_rim",main="Size of the protruding rim in each workshop")
dev.off()

defN4=read.csv("default_N4.csv")
vioplot2(defN4,"workshop","exterior_diam")

defN5=read.csv("testE_N5.csv")
vioplot2(defN5,"workshop","protruding_rim")

defN5=read.csv("lineC/lineC_100_N5.csv")
defN5=defN5[defN5$time == max(defN5$time),]
vioplot2(getLastIt(defN5),"workshop","exterior_diam")
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

YSLR_man   <-  function(){
verti=readFolder("verti/")
hori=readFolder("hori/")
horicube=readFolder("horiCub/")
horiM=readFolder("horiM/")
horiH=readFolder("horiH/")
horimas=readFolder("horimas/")

j=rbind(
	     varSim(getLastIt(verti),vari="protruding_rim"),
	     varSim(getLastIt(hori),vari="protruding_rim"),
	     varSim(getLastIt(horiH),vari="protruding_rim")
	     )
rownames(j)=c("VT","VT+HT(d)","VT+HT")
plotDensities(t(j),colnames(t(j)))

juntosPR=rbind(
	     varSim(getLastIt(verti),vari="protruding_rim"),
	     varSim(getLastIt(hori),vari="protruding_rim"),
	     varSim(getLastIt(horiH),vari="protruding_rim")
	     #varSim(getLastIt(horimas))
	     )
rownames(juntosPR)=c("VT","VT+HT(d)","VT+HT")
pdf("../../doc/YSLR_Manchester/images/PR_densities.pdf",pointsize=17)
plotDensities(t(juntosPR),colnames(t(juntosPR)))
abline(v=sd(tapply(emp$protruding_rim,emp$site,mean)),col="red",lwd=3)
text(sd(tapply(emp$protruding_rim,emp$site,mean))+0.8,.23,"dataset variation of means",srt=90,col="red",cex=.7)
dev.off()

juntos=rbind(
	     varSim(getLastIt(verti),vari="exterior_diam"),
	     varSim(getLastIt(hori),vari="exterior_diam"),
	     varSim(getLastIt(horiH),vari="exterior_diam")
	     )
rownames(juntos)=c("VT","VT+HT(d)","VT+HT")
pdf("../../doc/YSLR_Manchester/images/ED_densities.pdf",pointsize=17)
plotDensities(t(juntos),colnames(t(juntos)))
abline(v=sd(tapply(emp$exterior_diam,emp$site,mean)),col="red",lwd=3)
text(sd(tapply(emp$exterior_diam,emp$site,mean))+0.8,.25,"dataset variation of means",srt=90,col="red",cex=.7)
dev.off()

pdf("../../doc/YSLR_Manchester/images/PR_densities.pdf",pointsize=17)
vioplot3(t(juntosPR),ylim=c(0,,max(juntosPR)),ylab="Interworkshops variation (cm)",xlab="P(T)",xaxt="n")
abline(h=sd(tapply(emp$protruding_rim,emp$site,mean)),col="red",lwd=3)
text(sd(tapply(emp$protruding_rim,emp$site,mean))+0.8,.23,"dataset variation of means",srt=90,col="red",cex=.7)
dev.off()

juntos=rbind(
	     varSim(getLastIt(verti),vari="exterior_diam"),
	     varSim(getLastIt(hori),vari="exterior_diam"),
	     varSim(getLastIt(horiH),vari="exterior_diam")
	     )
rownames(juntos)=c("VT","VT+HT(d)","VT+HT")
pdf("../../doc/YSLR_Manchester/images/ED_densities.pdf",pointsize=17)
vioplot3(t(juntos),ylim=c(0,max(juntos)),ylab="Interworkshops variation (cm)",xlab="",xaxt="n")
abline(h=sd(tapply(emp$exterior_diam,emp$site,mean)),col="red",lwd=3)
text(sd(tapply(emp$exterior_diam,emp$site,mean))+0.8,.25,"dataset variation of means",srt=90,col="red",cex=.7)
dev.off()
}

vioplot2(getLastIt(verti),"workshop","exterior_diam")



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

varWorkshopTime<-function(data,vari="exterior_diam"){
    sapply(unique(data$time),function(i){
		     r=sd(tapply(data[data$time==i,vari],data$workshop[data$time==i],mean))
		     names(r)=i
		     return(r)
    })
}

varSim<-function(data,vari="exterior_diam"){
	sapply(unique(data$id),function(i){
	       tmp=data[data$id == i,]
	       varWorkshopTime(tmp,vari=vari)
    })
}

limitTimeStep<-function(data,timelist){
return(data[data$time %in% timelist ,])
}

plotDensities <- function(datas,epsilon,...){
    htcol=heat.colors(length(epsilon),alpha=1)
    names(htcol)=epsilon
    htcolF=heat.colors(length(epsilon),alpha=.5)
    names(htcolF)=epsilon
    densities=lapply(colnames(datas) ,function(i){density(datas[,i])})
    names(densities)=colnames(datas)
    rangex=range(lapply(densities,function(i)range(i$x)))
    rangey=range(lapply(densities,function(i)range(i$y)))
    par(mar=c(5,5,1,1))
    plot(density(datas),xlim=rangex,ylim=rangey,type="n",xlab="Variation of the mean size per workshop",main="",...)
    lapply(seq_along(densities),function(i){
	   polygon(densities[[i]],col=htcolF[names(densities)[i]],lwd=2)#,density=20,angle=45*i,border=htcol[names(densities)[i]])
#	   abline(v=mean(densities[[i]]$x),col=htcol[names(densities)[i]])
#	   text(mean(densities[[i]]$x),0,names(densities)[i],col=htcol[names(densities)[i]])
	})
    legend("topright",legend=epsilon,fill=htcolF,title="model")
}

