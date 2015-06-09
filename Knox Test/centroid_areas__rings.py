from datetime import date
from datetime import timedelta
from math import sqrt
import csv

def get_centroid_dict(source):

    centroid_dict = {}

    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            if not row["Block"] in centroid_dict.keys():
                X_coord = float(row["b_x_centro"])
                Y_coord = float(row["b_y_centro"])
                beat = row["Beat"]
                tract = row["TRACTCE10"]
                centroid_dict[row["TRACT_BLOC"]] = (X_coord, Y_coord, beat, tract)

    return centroid_dict

def get_crimes_list(source, centroid_dict):

    crimes = []         # Each entry is of the form:
                        # (days_from_end, distance_from_centroid, census_block)

    start_date = date(day=6, month=3, year=2015)
    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            try:
                x_coord = float(row["b_x_centro"])
                y_coord = float(row["b_y_centro"])

                ymd = row["ymd"]
                ymd_split = ymd.split('/')
                day = int(ymd_split[1])
                month = int(ymd_split[0])
                year = int(ymd_split[2])
                date_occurred = date(day=day, month=month, year=(year+2000))
                days_from_end = (start_date - date_occurred).days

                crimes.append((x_coord, y_coord, days_from_end))
            except ValueError:
                pass

    return crimes

def make_matrix(centroid_dict, crimes_list, time_threshold, space_list):

    # centroid dict is : "Census Block Name": (X, Y, beat)
    # crimes is a list: [(X, Y, days_from_end)]
    # time_threshold is number of days from the start that we look back.
    # space_list lists our space thresholds (e.g. [600, 1200, ..].)

    header = "beat,tract,block,days_from_end"
    for distance in space_list:
        header += ",{0}".format(distance)
    print header

    max_distance = space_list[len(space_list) - 1]

    for centroid in centroid_dict.keys():
        for days in range(time_threshold):
            crimes_found_list = [0 for distance in space_list]
            for crime in crimes_list:
                if crime[2] == days:
                    distance_from_centroid = sqrt((centroid_dict[centroid][0] - crime[0])**2 + (centroid_dict[centroid][1] - crime[1])**2)
                    if distance_from_centroid <= max_distance:
                        distance_bin = 0
                        while space_list[distance_bin] < distance_from_centroid:
                            distance_bin += 1
                        crimes_found_list[distance_bin] += 1
            beat = centroid_dict[centroid][2]
            tract = centroid_dict[centroid][3]
            print_line = "{0},{1},{2},t-{3}".format(beat, tract, centroid, days)
            for crimes in crimes_found_list:
                print_line += ",{0}".format(crimes)
            print print_line


if __name__ == "__main__":
    source = "chicago2015.csv"
    centroid_dict = get_centroid_dict(source)
    crimes = get_crimes_list(source, centroid_dict)
    time_threshold = 1
    space_list = [0, 600, 1200, 1800, 2400, 3000]
    make_matrix(centroid_dict, crimes, time_threshold, space_list)
