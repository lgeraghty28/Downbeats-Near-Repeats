
library("data.table")
library("ggplot2")
library("plyr")


setwd("/Users/jpheisel/Desktop/crime")

#data <- read.csv("chicago_crime.csv", nrows = 100000)
data_ <- fread("chicago_crime.csv")


# Subsetting
burgs <- subset(data_, data_$"Primary Type" == "BURGLARY")
sample_of_burgs <- burgs[ID %in% sample(burgs$ID, 175000, FALSE)]

# Get only date
burgs$date <- as.Date(burgs$Date, "%m/%d/%Y")

# Summary statistics
count(data_$"Primary Type")
count(burgs$Ward)
count(burgs$Beat)
count(burgs$District)



# Write out
write.csv(sample_of_burgs, "burgs.csv")
