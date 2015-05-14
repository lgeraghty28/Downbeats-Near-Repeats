#Code by Manuel Aragonés --- April 2015

rm(list=ls()) #clear environment

# Run libraries we will need
library(data.table)
library(ggplot2)
library(reshape)
library(httr)
library(jsonlite)
library(RSocrata)
library(dynlm)
library(randtests)

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
hour <- hour(lubdt)
weekday <- wday(lubdt)
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

#2.8 #For each Block, Aggregate the data by Ymd
rm(agg.by.ymd.block) #delete the data frame
agg.by.ymd.block <- aggregate(bdb$Count, list(ymd,Block), sum, na.rm=TRUE) 
colnames(agg.by.ymd.block) <- c("Date","Block","Number of Burglaries")
write.csv(agg.by.ymd.block, "mydfblock.csv")

summary(bdbCOMPLETEbyBLOCK$block)

# I the exported the file to Stata and with the following code I managed to fill missing values and dates
# generate date2 = date(date, "YMD")
# format date2 %tdNN/DD/CCYY
# xtset communityarea date2
# tsfill, full
# mvencode numberofburglaries, mv(0)
# export delimited using "/Users/maragones/Dropbox/00 R/CityLab/bdbCOMPLETE.csv", replace

# There is this code online but did not had time to make it work
# Link: http://www.enoriver.net/2015/02/09/r-version-of-tsfill-and-xfill-combined/

# Create a Vector of All Days Between Two Dates 
# link http://stackoverflow.com/questions/14450384/create-a-vector-of-all-days-between-two-dates/14450421#14450421
seq(as.Date("2001-01-01"), as.Date("2015-05-30"), by="days")
itemizeDates <- function(startDate="12-30-11", endDate="1-4-12", 
                         format="%m-%d-%y") {
  out <- seq(as.Date(startDate, format=format), 
             as.Date(endDate, format=format), by="days")  
  format(out, format)
}

itemizeDates(startDate="12-30-11", endDate="1-4-12")


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


# Create a dummy variable where there was a robbery in the day before within the CA The lag function is not working

tsset bdbCOMPLETE$date2 bdbCOMPLETE$burg.num
burg.num.lag0 <- bdbCOMPLETE$burg.num
burg.num.lag1 <- lag(bdbCOMPLETE$burg.num, k=60*60*24) 

this <- data.frame(bdbCOMPLETE$date2, burg.num.lag0, burg.num.lag1)
View(this)


#This is a linear regression for each of the Community Areas
fit <- 999
sig <- 999
nummodel <- 999
for (i in 1:5) {
  fit <- dynlm(bdbCOMPLETE$burg.num ~ L(bdbCOMPLETE$burg.num, 1), bdbCOMPLETE$CA==i, start = c(2012, 1), end = c(2014, 12))  
  significancy <- summary(fit)$coef[-1,4]
  append(sig, significancy, after=lenght(sig))
  append(nummodel, i, after=lenght(nummodel))
}




#it works without the loop
fit <- lm(burg.num.lag0 ~ burg.num.lag1, data=bdbCOMPLETE, CA==25)  
summary(fit)


library(plm)
attach(bdbCOMPLETE)
dfm <- dynlm(bdbCOMPLETE$burg.num ~ L(bdbCOMPLETE$burg.num, 1), bdbCOMPLETE$CA==25, start = c(2002, 1), end = c(2014, 12))  
summary(dfm)


plm(burg.num~ lag(burg.num,1), data = bdbCOMPLETE, index("CA", "date2"), model="within")


# Begin time series auto regressive model

dfm <- dynlm(bdbCOMPLETE$burg.num ~ L(bdbCOMPLETE$burg.num, 1), bdbCOMPLETE$CA==25)  
summary(dfm)


################################################################
################################################################
### Generate a Data Frame with Burglaries by CA to run time series analysis
### 
dfca <- data.frame(table(ymd, bdb$Community.Area))
colnames(dfca) <- c("Date", "Community.Area", "Burglaries")
View(dfca)
write.csv(dfca, "mydfca.csv")




plot <- qplot(date, psavert, data = economics, geom = "line") +
  ylab("Personal savings rate") +
  geom_hline(xintercept = 0, colour = "grey50")
plot
plot + scale_x_date(major = "10 years")
plot + scale_x_date(
  limits = as.Date(c("2004-01-01", "2005-01-01")),
  format = "%Y-%m-%d"
)










#example of a Panel data http://www.rdocumentation.org/packages/qogdata/functions/xtset
# Load QOG demo datasets.
data(qog.demo)
# Set xtdata attribute on QOG time series.
QOG = xtset(qog.ts.demo)
# Set xtdata attribute on recent years.
QOG.200x = xtset(subset(qog.ts.demo, year > 1999))
# Manually set xtdata attribute for UDS dataset.
UDS = get_uds()
UDS = xtset(UDS,
            data = c("ccodecow", "year"),
            spec = c("cown", "year"),
            type = "country",
            name = "Unified Democracy Scores"
)

###### For my excel graphs
#Graph 1
rm(agg.by.year) #delete the data frame
agg.by.year <- aggregate(bdb$Count, list(year), sum, na.rm=TRUE) 
colnames(agg.by.year) <- c("year","Number of Burglaries")
write.csv(agg.by.year, "mydfdate.csv")

#Graph 2
rm(agg.by.ym) #delete the data frame
agg.by.ym <- aggregate(bdb$Count, list(year,month), sum, na.rm=TRUE) 
colnames(agg.by.ym) <- c("year", "month","Number of Burglaries")
write.csv(agg.by.ym, "mydfdateym.csv")

# Graph 3
rm(agg.by.desc) #delete the data frame
agg.by.desc <- aggregate(bdb$Count, list(bdb$Description), sum, na.rm=TRUE) 
colnames(agg.by.desc) <- c("Description of burglary")
write.csv(agg.by.desc, "mydfdatedesc.csv")

# Graph 4
rm(agg.by.hour) #delete the data frame
agg.by.hour <- aggregate(bdb$Count, list(hour), sum, na.rm=TRUE) 
colnames(agg.by.hour) <- c("Hour of burglary")
write.csv(agg.by.hour, "mydfdatehour.csv")

# Graph 5
rm(agg.by.weekday) #delete the data frame
agg.by.weekday <- aggregate(bdb$Count, list(weekday), sum, na.rm=TRUE) 
colnames(agg.by.weekday) <- c("Day of the week")
write.csv(agg.by.weekday, "mydfweekday.csv")

#Graph by block
rm(agg.by.block) #delete the data frame
agg.by.block <- aggregate(bdb$Count, list(bdb$Block),sum , na.rm=TRUE) 
colnames(agg.by.block) <- c("Block","Numberofburglaries")
write.csv(agg.by.block, "mydfblocks.csv")

#Top block
topblock <- subset(bdb, Block=="078XX S SOUTH SHORE DR") #Create a subset database
topblock["Count"] <-1
lubdttop <- mdy_hms(topblock$Date)
ymd2 <- format(lubdttop, "%Y-%m-%d")
agg.topblock <- aggregate(topblock$Count, list(ymd2),sum , na.rm=TRUE) 
write.csv(agg.topblock, "topblock.csv")

###### Regression by CA
fit <- lm(CAdummycomplete$CA1 ~ CAdummycomplete$CA1.L1)
significancy <- summary(fit)$coef[-1,4]
print(1, significancy)
summary(fit)

#### Runs test
for (i in 1:77) {
  runs <- runs.test(CAdummycomplete$CAi, alternative="left.sided", plot=F)
  summary(runs)
}

runs.test(CAdummycomplete$CA1, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA2, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA3, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA4, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA5, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA6, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA7, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA8, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA9, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA10, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA11, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA12, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA13, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA14, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA15, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA16, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA17, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA18, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA19, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA20, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA21, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA22, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA23, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA24, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA25, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA26, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA27, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA28, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA29, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA30, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA31, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA32, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA33, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA34, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA35, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA36, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA37, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA38, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA39, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA40, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA41, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA42, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA43, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA44, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA45, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA46, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA47, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA48, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA49, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA50, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA51, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA52, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA53, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA54, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA55, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA56, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA57, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA58, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA59, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA60, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA61, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA62, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA63, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA64, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA65, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA66, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA67, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA68, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA69, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA70, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA71, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA72, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA73, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA74, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA75, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA76, alternative="left.sided", plot=F)
runs.test(CAdummycomplete$CA77, alternative="left.sided", plot=F)