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
year <- year(lubdt)
month <- month(lubdt)
week <- week(lubdt)
dayofyear <- yday(lubdt)

#In order to use aggrgate to count
bdb["Count"] <-1
#Aggregate the data by Community area
rm(agg.by.ca)
agg.by.ca <- aggregate(bdb$Count, list(bdb$Community.Area), sum) 
colnames(agg.by.day.ca) <- c("Community Area", "Number of Burglaries")
sort(agg.by.day.ca$"Number of Burglaries", decreasing=TRUE )
write.csv(agg.by.day.ca, "mydf1.csv") #write CSV file to see if the data works

agg.by.ca$x1 <- table(agg.by.ca$x)



#A series of graphs
d <- ggplot(data=agg.by.day.ca, aes(x="Group.1", y="x"))
d + geom_line






#When adding wards, the numbers do not add up, my intuition is the NA's

#Aggregate the data by Year, Month, Beat 
agg.by.beat <- aggregate(bdb$Primary.Type, list(year, month, Beat), summary, bdb$Primary.Type=="BURGLARY")
#Aggregate the data by Date & Community.Area
agg.by.ca <- aggregate(bdb$Primary.Type, list(dt, Ward), summary, bdb$Primary.Type=="BURGLARY")

#A series of graphs
ggplot(data=bdb, aes(x=lubdt, y=Primary.Type, group=District, colour=District)) +
  geom_line() +
  geom_point()




#Trying to run a linear model with lags
dfm <- dynlm(agg.by.ca$x ~ L(agg.by.ca$x, 1) + L(agg.by.ca$x, 2), agg.by.ca$Group.2==1) 

sum.by.type <- summary(crimedb$Primary.Type, Index=crimedb$Primary.Type)
table(crimedb$Year, crimedb$Primary.Type=="BURGLARY")
table(crimedb$Year, crimedb$Primary.Type=="BATTERY")
table(crimedb$Community.Area, crimedb$Primary.Type=="BURGLARY")
table(crimedb$Community.Area, crimedb$Primary.Type=="BATTERY")

