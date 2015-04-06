
library("data.table")
library("ggplot2")
library("plyr")


setwd("/Users/jpheisel/Desktop/crime")

#data <- read.csv("chicago_crime.csv", nrows = 100000)
data_ <- fread("chicago_crime.csv")


# Subsetting
burgs <- subset(data_, data_$"Primary Type" == "BURGLARY")
sample_of_burgs <- burgs[ID %in% sample(burgs$ID, 175000, FALSE)]


# Summary statistics
count(data_$"Primary Type")


# Write out
write.csv(sample_of_burgs, "burgs.csv")
