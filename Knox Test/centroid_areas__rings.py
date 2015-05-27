from datetime import date
from datetime import timedelta
from math import sqrt
import csv

def get_centroid_dict(source):

    centroid_dict = {}

    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            if not row["TRACT_BLOC"] in centroid_dict.keys():
                centroid_dict[row["TRACT_BLOC"]] = (float(row["b_x_centro"]), float(row["b_y_centro"]), row["COMMAREA"])

    return centroid_dict

def get_crimes_list(source, centroid_dict):

    crimes = []         # Each entry is of the form:
                        # (days_from_end, distance_from_centroid, census_block)

    start_date = date(day=25, month=3, year=2015)
    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            try:
                block = row["TRACT_BLOC"]
                x_coord = float(row["X_Coordina"])
                y_coord = float(row["Y_Coordina"])

                ymd = row["ymd"]
                ymd_split = ymd.split('/')
                day = int(ymd_split[1])
                month = int(ymd_split[0])
                year = int(ymd_split[2])
                date_occurred = date(day=day, month=month, year=year)
                days_from_end = abs((start_date - date_occurred).days)

                crimes.append((days_from_end, x_coord, y_coord))
            except ValueError:
                pass

    return crimes

def make_matrix(centroid_dict, crimes, time_threshold, space_list):

    # centroid_dict is : ["Block Name": (X, Y, Community_Area)]
    # crimes is a list: [(X, Y, days_from_end)]
    # time_threshold is number of days from the start that we look back.
    # space_list lists our space thresholds (e.g. 600, 1200 ...)

    start_date = date(day=25, month=3, year=2015)

    header = "community_area,block,days_from_end"
    for distance in space_list:
        header += ",{0}".format(distance)
    print header

    max_distance = space_list[len(space_list) -1]

    for centroid in centroid_dict.keys():
        start_date = date(day=25, month=3, year=2015)
        community_area = centroid_dict[centroid][2]
        crimes_found

if __name__ == "__main__":
    source = "chicago2010-15(1).csv"
    centroid_dict = get_centroid_dict(source)
    crimes = get_crimes_list(source, centroid_dict)
    time_threshold = 15
    space_list = [600, 1200, 1800, 2400, 3000]
    make_matrix(centroid_dict, crimes, time_threshold, space_list)
