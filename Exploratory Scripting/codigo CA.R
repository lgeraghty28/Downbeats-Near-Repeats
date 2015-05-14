library(data.table)
library(lubridate)


setwd("C:/Users/titog/Desktop/city lab")
popandpov <- fread("PopAndPov.csv")
popandpov$V10 <- popandpov$V11 <- popandpov$V12 <- popandpov$V13 <- popandpov$V14 <- popandpov$V15 <- NULL

crimes <- fread("Crimes_-_2001_to_present.csv")
setnames(crimes,"Primary Type","primarytype")



crimes$Date <- mdy_hms(crimes$Date)
crimes$day <- weekdays(crimes$Date)
crimes$hour <- hour(crimes$Date)
crimes$year <- year(crimes$Date)
crimes$month <- month(crimes$Date)
crimes$week<- week(crimes$Date)
crimes$day<- yday(crimes$Date)
crimes$ymd <- substring(crimes$Date, 1, 10)

crimes <- subset(crimes, crimes$year == 2014)
cr<-crimes
ca<-data.frame(table(cr$"Community Area"))
ca<-subset(ca,ca$Var1!=0)
setwd("C:/Users/titog/Desktop/city lab/knox test/ca files")

###drop columns we will not use
attach(cr)

cr$"ID" <- cr$"Case Number" <- cr$ "Date"<-cr$"Block"<-cr$"IUCR"<-cr$"primarytype"<-cr$"Description"<-cr$"Location Description"<-cr$"Arrest"<-cr$"Domestic"<-cr$"Beat"<-cr$"District" <- NULL
cr$"Ward" <-cr$"FBI Code"<-cr$"Year"<-cr$"Updated On"<-cr$"Latitude" <-cr$"Longitude"<-NULL
cr$"Location"<-cr$"day" <-cr$"hour"<-cr$"year"<-cr$"month"<-cr$"week"<- NULL
cr$ymd=ymd(cr$ymd)


for (x in ca$Var1){
  dfi <- subset(cr, cr$"Community Area"==x)
  dfi$"Community Area"<-NULL
  write.csv(dfi, file = paste("ca", x,".csv", sep = ""), row.names=FALSE)
 
}


caa25<-subset(crimes, crimes$month>=7)
dfi <- subset(caa25, caa25$"Community Area"==25)
dfi$"Community Area"<-NULL
write.csv(dfi, file = paste("caa", 25,".csv", sep = ""), row.names=FALSE)