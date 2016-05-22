

analyseModel<-function(){
model=read.csv("result.csv") ;  
model=model[model$time >= max(model$time)-1000,]; 
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
}

analyseRealData<-function(){

emp=read.csv("data/dres.csv")
	boxplot(emp$exterior_diam ~ emp$site)
	cov(emp$rim_h,emp$rim_w)
	cor(emp$rim_h,emp$rim_w)
	cov(emp$exterior_diam,emp$rim_w)
	cor(emp$exterior_diam,emp$rim_h)
	plot(emp$exterior_diam~emp$inside_diam)
	cor(emp$exterior_diam,emp$inside_diam)
	abline(
	       lm(emp$exterior_diam~emp$rim_w)

}
