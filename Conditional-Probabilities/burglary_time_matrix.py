import csv
from datetime import date, timedelta

burglaries = []

with open ("crime5051_ymd.csv", "rU") as csvfile:
    crimereader = csv.DictReader(csvfile)
    i=0
    for row in crimereader:
        day_string =  row['ymd'].split('/')
        day = date(month=int(day_string[0]), day=int(day_string[1]), year=(2000 + int(day_string[2])))
        i += 1
        burglaries.append((i, day))

topstring = ""
for day in burglaries:
    topstring += ",{0}".format(day[0])

topstring+="\n"

differences = ""
for rowday in burglaries:
    differences+= "{0}".format(rowday[0])
    for columnday in burglaries:
        difference = (columnday[1]-rowday[1]).days
        differences += ",{0}".format(difference)

    differences+="\n"

with open ("time_crime5051.csv", "w") as f:
    f.write(topstring + differences)
