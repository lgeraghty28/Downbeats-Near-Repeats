##### sample baseline for census tracts in 1-5 communities in 2014 #####
setwd('/Users/linxia/Desktop/city')
all<-read.csv('omi-chicago2010-15.csv') #### (make sure csv date format in 'yyyy-mm-dd') all burglary in chicago 2010-15, with cases lacking location information omitted

sample<-all[all$Year==2014 & all$Community_<=5,]
attach(sample)

##### getting months in 2014 
ymd<-as.Date(ymd) ### this step must be done before installing lubridate. Otherwise the data type turns into closure and cannot be turned into dates 

install.packages('lubridate')
library(lubridate)
sample<-data.frame(sample,month(ymd)) #### a new colume of month in sample table

#### 1. empty matrix 
attach(sample)
matrix<-matrix(0,nrow=length(unique(TRACTCE10)),ncol=12,byrow=T,dimnames=list(c(unique(TRACTCE10)),seq(1,12,1)))

#### 2. aggregates b counts per tract by month 
counts<-aggregate(cbind(binary),by=list(TRACTCE10,month.ymd.),FUN='sum')

#### 3. filling matrix
for (i in 1:length(unique(TRACTCE10))){
  for (j in 1:12){
    for (n in 1:nrow(counts)){
      if (counts[n,1]==rownames(matrix)[i]) {
        if (colnames(matrix)[j]==counts[n,2]) {
          matrix[i,j]<-counts[n,3]
        }
      }
    }
  }
}

#### 4. calculate the probability of burglary happens per day by month in 2014 
length(unique(Community_))
matrix2<-matrix(0,nrow=length(unique(TRACTCE10)),ncol=4,dimnames=list(NULL,c('Jan_Mar_ave','Apr_Jun_ave','Jul_Sep_ave','Oct_Dec_ave')))

for (i in 1:length(unique(TRACTCE10))){
  matrix2[i,(1:4)]<-c(round(sum(matrix[i,(1:3)])/90,digits=6),round(sum(matrix[i,(4:6)])/90,digits=6),round(sum(matrix[i,(7:9)])/90,digits=6),round(sum(matrix[i,(10:12)])/90,digits=6))
}

matrix2<-data.frame(unique(TRACTCE10),matrix2)
names(matrix2)[names(matrix2)=="unique.TRACTCE10."] <- "tract"

write.csv(matrix2, file='sample_baseline.csv')
