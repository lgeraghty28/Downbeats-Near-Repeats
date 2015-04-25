import csv
from datetime import date, timedelta

crimes = []
blocks = []
dates = []

with (open("crime5051_ymd.csv", "rU")) as csvfile:
    crimereader = csv.DictReader(csvfile)
    i=0
    for row in crimereader:
        #print row['ymd'] + "\t" + row['block']
        day_string = row['ymd'].split('/')
        day = date(month=int(day_string[0]), day=int(day_string[1]), year=(2000 + int(day_string[2])))
        block = row['block']
        crimes.append((block, day))
        if not block in blocks:
            blocks.append(block)
        if not day in dates:
            dates.append(day)

num_crimes = []

blocks_with_proximals = 0

for block in blocks:
    block_crimes = []
    for crime in crimes:
        if crime[0] == block:
            block_crimes.append(crime[1])

    num_crimes.append(len(block_crimes))

    proximal = 0

    has_proximal = False
    if len(block_crimes) > 1:
        block_crimes.sort()
        for crime in enumerate(block_crimes):
            try:
                if block_crimes[crime[0] + 1] - crime[1] < timedelta(days=7):
                    #print "First crime: {0}\t Second crime: {1}". format(crime[1], block_crime[crime[0]+1])
                    proximal += 1
                    has_proximal = True
            except IndexError:
                pass

        if has_proximal:
            blocks_with_proximals +=1

print "Blocks with crimes: {0}".format(len(blocks))

print "Blocks with proximals: {0}".format(blocks_with_proximals)

print "First crime {0}".format(min(dates))
print "Last crime {0}".format(max(dates))
print "Max number of crimes: {0}".format(max(num_crimes))

#output:
    #blocks with crimes: 326
    #first crime: 2010-01-04
    #last crime: 2015-03-25
    #Max number of crimes on one block: 25
