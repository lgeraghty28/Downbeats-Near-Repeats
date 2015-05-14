import csv
from datetime import date, timedelta

crimes = []
blocks = []
dates = []

with open("crime5051_ymd.csv", "rU") as csvfile:
    crimereader = csv.DictReader(csvfile)
    i = 0
    for row in crimereader:
        #print row['ymd'] + "\t" + row['block']
        day_string =  row['ymd'].split('/')
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
                    #print "First crime: {0}\t Second crime: {1}".format(crime[1], block_crimes[crime[0]+1])
                    proximal += 1
                    has_proximal = True
            except IndexError:
                pass

    if has_proximal:
        blocks_with_proximals += 1

print "Blocks with crimes: {0}".format(len(blocks))

print "Blocks with proximals: {0}".format(blocks_with_proximals)

print "First crime {0}".format(min(dates))

# Create an m by (n by n) nested matrix where m is the number of blocks in the
# sample and n is the number of weeks. In each row, we have [t, t+1, t+2 ...] where
# t = 1 if a crime occurred in the current week and t = 0 if it did not.
# t+1 is the same, but for the following week.

conditional_matrix = []                     # The final output matrix
csv_string = ""
for block in blocks:                        # make a matrix for each block
    block_crimes = []                       # list of crimes that occurred on each block
    for crime in crimes:
        if block == crime[0]:
            block_crimes.append(crime[1])   # Add date the crime occurred
    if not block_crimes == []:
        block_crimes.sort()                     # sort block crimes by date
        current_date =  min(dates)              # Set current to the beginning of our time sample
        block_array = []                        # 1s and 0s for each week in the sample
        while current_date < max(dates):        # begin at the beginning of time in the sample and end at the end of the sample
            crime_in_week = False               # Assume no crime
            for count in range(7):
                if not block_crimes == [] and block_crimes[0] == current_date:
                    while not block_crimes == [] and block_crimes[0] == current_date:
                        block_crimes.pop(0)                 # Removes the date found so that we don't miss the next one
                    crime_in_week = True
                current_date += timedelta(days=1)           # Look at the next day
            if crime_in_week:
                block_array.append(1)
            else:
                block_array.append(0)
        block_matrix = []                                   # Change to 2 dimensional
        for week in enumerate(block_array):                 # Enumerate gives (index, value) tuple
            next_week = block_array[week[0]:]               # next week = [t, t+1, t+2...] where t is the column number
            block_matrix.append(next_week)
            while len(next_week) < len(block_array):        # Zero padding to equalize length
                next_week.append(0)

        for i in block_matrix:
            csv_string += "{0}".format(block)
            for j in i:
                csv_string += ",{0}".format(j)
            csv_string += "\n"

        conditional_matrix.append(block_matrix)             # Add the block's matrix to the overall matrix.


# Should give the csv want, but with ' ' delimiters instead of ','
for block in enumerate(blocks):
    for week in enumerate(block_array):
        print "{0} {1}".format(block, conditional_matrix[block[0]][week[0]])


print "Last crime {0}".format(max(dates))
print "Max number of crimes: {0}".format(max(num_crimes))

with open('50_51.csv', 'w') as f:
    f.write(csv_string)
