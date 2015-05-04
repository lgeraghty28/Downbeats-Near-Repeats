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
                crimes.append((xcoord, ycoord, day))
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
    for crime in crimes:
        if abs((crime[2] - current_date).days) >= 7:
            weekly_crime.append(crime)
        else:
            while abs((crime[2] - current_date).days) < 7:
                total_weeks += 1
                current_date = current_date + timedelta(days=7)
            locs = []
            for burglary in weekly_crime:
                for loc in locs:
                    distance = sqrt((burglary[0] - loc[0])**2 + (burglary[1] - loc[1])**2)
                    if (distance < threshold):
                        proximal = True
                        weeks_with_proximal_crime += 1
                        break
                if proximal:
                    break
                locs.append((burglary[0], burglary[1]))

            weekly_crime = []
            proximal = False

    print("Weeks with proximal crimes: {0}".format(weeks_with_proximal_crime))


if __name__ == "__main__":
    crimes = get_crime_list("crime5051_ymd.csv")
    for i in range(10):
        parse_crimes(crimes, 300*i)
