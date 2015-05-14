import csv
from datetime import date, timedelta
from math import sqrt

def get_crime_list(source):

    crimes = []

    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            try:
                day_string = row["ymd"].split('/')
                day = date(month=int(day_string[0]), day=int(day_string[1]), year=(2000 + int(day_string[2])))
                xcoord = int(row["x.coordinate"])
                ycoord = int(row["y.coordinate"])
                iden = row["id"]
                crimes.append((xcoord, ycoord, day, iden))
            except ValueError:
                pass
    return crimes

def parse_crimes(crimes, threshold):

    crimes = sorted(crimes, key=lambda crime: crime[2])
    total_weeks = 1
    weeks_with_proximal_crime = 0
    current_date = crimes[0][2]
    weekly_crime = []
    proximal = False

    crime_dict = {}
    for crime in crimes:
        crime_id = crime[3]
        crime_dict[crime_id] = False

    for crime in crimes:
        if abs((crime[2] - current_date).days) >= 7:
            weekly_crime.append(crime)
        else:
            while abs((crime[2] - current_date).days) < 7:
                total_weeks += 1
                current_date = current_date + timedelta(days=7)
            locs = {}
            for burglary in weekly_crime:
                for id in locs.keys():
                    loc = locs[id]
                    distance = sqrt((burglary[0] - loc[0])**2 + (burglary[1] - loc[1])**2)
                    if (distance <= threshold):
                        proximal = True
                        weeks_with_proximal_crime += 1
                        crime_dict[id] = True
                        crime_dict[burglary[3]] = True

                locs[burglary[3]] = (burglary[0], burglary[1])

            weekly_crime = []
            proximal = False


    proximals_count = 0
    for key in crime_dict.keys():
        if crime_dict[key]:
            proximals_count += 1

    proximals_false = 0
    for key in crime_dict.keys():
        if not crime_dict[key]:
            proximals_false+=1

    print("We have {0} crimes with proximals when using a threshold of {1} feet".format(proximals_count, threshold))
    print("We have {0} crimes without".format(len(crime_dict.keys()) - proximals_count))
    print("We have {0} crimes without proximals".format(proximals_false, threshold))

if __name__ == "__main__":
    crimes = get_crime_list("crime5051_ymd.csv")
    for i in range(10):
        parse_crimes(crimes, 300*i)
