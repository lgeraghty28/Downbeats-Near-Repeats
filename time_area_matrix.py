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

def parse_crimes(crimes, time_threshold, space_threshold):

    crimes = sorted(crimes, key=lambda crime: crime[2])
    
    csv_string = "id"
    total_time_periods = abs((crimes[0][2] - crimes[len(crimes)-1][2]).days) / time_threshold
    for periods in range(total_time_periods):
        csv_string += ",{0}".format(period+1)
    csv_string += "\n"

    for crime_area in crimes:
        area_id = crime_area[3]
        csv_string += "{0}".format(area_id)
        current_date = crimes[0][2]
        crime_this_period = False
        for crime in crimes:
            if abs((crime[2] - current_date).days) > time_threshold:
                while abs((crime[2] - current_date).days) > time_threshold:
                    if crime_this_period:
                        csv_string += ",1"
                    else:
                        csv_string += ",0"
                    crime_this_period = False
                    current_date = current_date + timedelta(days=time_threshold)
            distance = sqrt((crime[0] - crime_area[0])**2 + (crime[1] - crime_area[1])**2)
            if distance < space_threshold:
                crime_this_period = True
        csv_string += "\n"

    csv_file_name = "days_{0}_by_space_{1}.csv".format(time_threshold, space_threshold)
    with open(csv_file_name, "w") as f:
        f.write(csv_string)

if __name__ == "__main__":
    crimes = get_crime_list("crime5051_ymd.csv")
    time_threshold = 7
    space_threshold = 300
    parse_crimes(crimes, time_threshold, space_threshold)
