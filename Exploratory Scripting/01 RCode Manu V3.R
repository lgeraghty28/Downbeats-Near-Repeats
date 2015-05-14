rm(list=ls()) #clear environment
library(data.table)
library(ggplot2)
library(reshape)
library(httr)
library(jsonlite)
library(RSocrata)
library(dynlm)
## Not working... crimedataset <- read.socrata('https://data.cityofchicago.org/resource/ijzp-q8t2')
#Crimes_._2001_to_present <- read.csv("~/Dropbox/00 R/CityLab/Crimes_-_2001_to_present.csv")
#View(Crimes_._2001_to_present)

crimedb <- read.csv("~/Dropbox/00 R/CityLab/crimedb.csv") #Open database
bdb <- subset(crimedb, Primary.Type=="BURGLARY") #Create a subset database
write.csv(bdb, "bdb.csv") 

rm(crimedb) #remove the complete crime database

attach(bdb)

length(ID) # Number of observations
dim(bdb) # number of obs and number of variables

#To choose the most disaggregated spatial unit 
length(unique(Block)) #37,575
length(unique(Beat))     #300
length(unique(Community.Area)) #78
length(unique(Ward)) #51
length(unique(District)) #24

#Unique events and time points
length(unique(ID))    #339,778
length(unique(Date))  #238,243

# Preparing data to use date functions
library(lubridate)
lubdt <- mdy_hms(bdb$Date) #Lubridate package for date functions, eg. extract day
ymd <- format(lubdt, "%Y-%m-%d")
year <- year(lubdt)
month <- month(lubdt)
week <- week(lubdt)
dayofyear <- yday(lubdt)

#In order to use aggregate to count
bdb["Count"] <-1

#2.1 #Aggregate the data by Community area
rm(agg.by.ca) #delete the data frame
agg.by.ca <- aggregate(bdb$Count, list(bdb$Community.Area), sum) 
colnames(agg.by.day.ca) <- c("Community Area", "Number of Burglaries")
sort(agg.by.day.ca$"Number of Burglaries", decreasing=TRUE ) # Top CA 43, Austin; 24...
write.csv(agg.by.day.ca, "mydf1.csv") #write CSV file to see if the data works

#2.2 #Aggregate the data by Community area & year
rm(agg.by.ca) #delete the data frame
agg.by.year.ca <- aggregate(bdb$Count, list(bdb$Community.Area, year), sum) 
colnames(agg.by.year.ca) <- c("Community Area", "Year","Number of Burglaries")
# sort(agg.by.year.ca$"Number of Burglaries", decreasing=TRUE ) # Top CA 43, Austin; 24, ?
write.csv(agg.by.day.ca, "mydf1.csv") #write CSV file to see if the data works

#2.3 #For each CA, Aggregate the data by year&week
rm(agg.by.year.week.ca) #delete the data frame
agg.by.year.week.ca <- aggregate(bdb$Count, list(year,week,Community.Area), sum, na.rm=TRUE) 
colnames(agg.by.year.week.ca) <- c("Year","Week","Community Area","Number of Burglaries")
write.csv(agg.by.year.week.ca, "mydf2.csv")

#2.4 #For each CA, Aggregate the data by year&DAY because by week we have too many ones
rm(agg.by.year.day.ca) #delete the data frame
agg.by.year.day.ca <- aggregate(bdb$Count, list(dayofyear,year,Community.Area), sum, na.rm=TRUE) 
colnames(agg.by.year.day.ca) <- c("Day of Year", "Year","Community Area","Number of Burglaries")
write.csv(agg.by.year.day.ca, "mydf3.csv")

#2.5 #For each CA, Aggregate the data by year&DAY because by week we have too many ones
rm(agg.by.year.day.ca) #delete the data frame
agg.by.year.day.ca <- aggregate(bdb$Count, list(dayofyear,year,Community.Area), sum, na.rm=TRUE) 
colnames(agg.by.year.day.ca) <- c("Day of Year", "Year","Community Area","Number of Burglaries")
write.csv(agg.by.year.day.ca, "mydf3.csv")

#2.6 #For each CA, Aggregate the data by date because by week we have too many ones
rm(agg.by.year.date.ca) #delete the data frame
agg.by.year.date.ca <- aggregate(bdb$Count, list(lubdt,Community.Area), sum, na.rm=TRUE) 
colnames(agg.by.year.date.ca) <- c("Date","Community Area","Number of Burglaries")
write.csv(agg.by.year.date.ca, "mydfdate.csv")

#2.7 #For each CA, Aggregate the data by Ymd
rm(agg.by.ymd.ca) #delete the data frame
agg.by.ymd.ca <- aggregate(bdb$Count, list(ymd,Community.Area), sum, na.rm=TRUE) 
colnames(agg.by.ymd.ca) <- c("Date","Community Area","Number of Burglaries")
write.csv(agg.by.ymd.ca, "mydfdate.csv")

# I the exported the file to Stata and with the following code I managed to fill missing values and dates
# generate date2 = date(date, "YMD")
# format date2 %tdNN/DD/CCYY
# xtset communityarea date2
# tsfill, full
# mvencode numberofburglaries, mv(0)
# export delimited using "/Users/maragones/Dropbox/00 R/CityLab/bdbCOMPLETE.csv", replace

# There is this code online but did not had time to make it work
# Link: http://www.enoriver.net/2015/02/09/r-version-of-tsfill-and-xfill-combined/
myXTFill <- function(x) {
  dt     <- copy(x)
  xtkeys <- c('zip.cd','cal.dt')
  clkeys <- c('zip.cd','dma.cd')
  xtfull <- CJ(unique(x[,zip.cd]),unique(x[,cal.dt]))
  clfull <- unique(subset(x,select=c(zip.cd,dma.cd)))
  setnames(xtfull,c('V1','V2'),xtkeys)
  setkeyv(xtfull,xtkeys)
  setkeyv(dt,xtkeys)
  setkeyv(clfull,clkeys)
  xtfull <- subset(merge(xtfull,dt,all=TRUE),select=-dma.cd)
  xtfull <- merge(xtfull,clfull,all=TRUE)
}


# Import complete dataset
rm(bdbCOMPLETE)
bdbCOMPLETE <- read.csv("~/Dropbox/00 R/CityLab/bdbCOMPLETE.csv", header=TRUE)
bdb.dt <- mdy(bdbCOMPLETE$date2) #%tdNN/DD/CCYY
colnames(bdbCOMPLETE) <- c("V1","originaldate","CA", "burg.num", "date2")


# Create a dummy variable where there was a robbery in the day before within the CA
burg.num.lag0 <- bdbCOMPLETE$burg.num
burg.num.lag1 <- lag(bdbCOMPLETE$burg.num,1) 
if(burg.num.lag0*burg.num.lag1>0){dummy <- 1} else {dummy <- 0)}, 1 else 0))
dummy <- if(burg.num.lag0*burg.num.lag1>0, 1 else 0)
df1 <- c(burg.num.lag0, dummy)


library(plm)
attach(bdbCOMPLETE)
plm(burg.num~ lag(burg.num,1), data = bdbCOMPLETE, index("CA", "date2"), model="within")


# Begin setting up panel data frame for Linear Autoregressive model
dfm <- dynlm(bdb.dt$numberofburglaries ~ L(bdb.dt$numberofburglaries, 1) + L(bdb.dt$numberofburglaries, 2))  


#A series of graphs
ggplot(data=agg.by.day.ca, aes(x=x, y=Group.1, colour=District)) +
  geom_line() +
  geom_point()







#When adding wards, the numbers do not add up, my intuition is the NA's

#A series of graphs
ggplot(data=bdb, aes(x=lubdt, y=Primary.Type, group=District, colour=District)) +
  geom_line() +
  geom_point()




#Trying to run a linear model with lags


table(crimedb$Year, crimedb$Primary.Type=="BURGLARY")
table(crimedb$Year, crimedb$Primary.Type=="BATTERY")
table(crimedb$Community.Area, crimedb$Primary.Type=="BURGLARY")
table(crimedb$Community.Area, crimedb$Primary.Type=="BATTERY")

