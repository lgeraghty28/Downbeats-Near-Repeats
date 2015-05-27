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
                centroid_dict[row["Block"]] = (float(row["TRACT_CENT"]), float(row["TRACT_CE_1"]), row["Community"])

    return centroid_dict

def get_crimes_list(source, centroid_dict):

    crimes = []         # Each entry is of the form:
                        # (days_from_end, distance_from_centroid, census_block)

    start_date = date(day=25, month=3, year=2015)
    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            try:
                block = row["Block"]
                x_coord = float(row["X_Coordina"])
                y_coord = float(row["Y_Coordina"])
                distance_from_centroid = sqrt((x_coord - centroid_dict[block][0])**2 +
                                              (y_coord - centroid_dict[block][1])**2)

                ymd = row["ymd"]
                ymd_split = ymd.split('/')
                day = int(ymd_split[1])
                month = int(ymd_split[0])
                year = int(ymd_split[2])
                date_occurred = date(day=day, month=month, year=year)
                days_from_end = abs((start_date - date_occurred).days)

                crimes.append((days_from_end, distance_from_centroid, block))
            except ValueError:
                pass

    return crimes

def make_matrix(centroid_dict, crimes, time_threshold, space_list):

    # time_threshold is number of days from the start that we look back.
    # space_list lists our space thresholds (e.g. 600, 1200 ...)

    start_date = date(day=25, month=3, year=2015)

    header = "community_area,block,days_from_end"
    for distance in space_list:
        header += ",{0}".format(distance)
    print header

    for block in centroid_dict.keys():
        community_area = centroid_dict[block][2]
        crimes_found_list = [0 for distance in space_list]
        for day in range(time_threshold + 1):
            print_line = "{2},{0},t-{1}".format(block, day, community_area)
            for distance in enumerate(space_list):
                for crime in crimes:
                    if crime[2] == block and crime[0] == day and distance[1] > crime[1]:
                        crimes_found_list[distance[0]] += 1
            if (1 + day) % 3 == 0:
                for crimes_found in crimes_found_list:
                    print_line += ",{0}".format(crimes_found)
                print print_line
                crimes_found_list = [0 for distance in space_list]


if __name__ == "__main__":
    source = "cent_5051.csv"
    centroid_dict = get_centroid_dict(source)
    crimes = get_crimes_list(source, centroid_dict)
    time_threshold = 15
    space_list = [600, 1200, 1800, 2400, 3000]
    make_matrix(centroid_dict, crimes, time_threshold, space_list)
