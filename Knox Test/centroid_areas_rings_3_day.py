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
                X_coord = float(row["TRACT_CENT"])
                Y_coord = float(row["TRACT_CE_1"])
                community_area = row["Community"]
                centroid_dict[row["Block"]] = (X_coord, Y_coord, community_area)

    return centroid_dict

def get_crimes_list(source, centroid_dict):

    crimes = []         # Each entry is of the form:
                        # (days_from_end, distance_from_centroid, census_block)

    start_date = date(day=25, month=3, year=2015)
    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            try:
                x_coord = float(row["X_Coordina"])
                y_coord = float(row["Y_Coordina"])

                ymd = row["ymd"]
                ymd_split = ymd.split('/')
                day = int(ymd_split[1])
                month = int(ymd_split[0])
                year = int(ymd_split[2])
                date_occurred = date(day=day, month=month, year=year)
                days_from_end = abs((start_date - date_occurred).days)

                crimes.append((x_coord, y_coord, days_from_end))
            except ValueError:
                pass

    return crimes

def make_matrix(centroid_dict, crimes_list, time_threshold, space_list):

    # centroid dict is : "Block Name": (X, Y, Community_Area)
    # crimes is a list: [(X, Y, days_from_end)]
    # time_threshold is number of days from the start that we look back.
    # space_list lists our space thresholds (e.g. [600, 1200, ..].)
    
    header = "community_area,block,days_from_end"
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

            community_area = centroid_dict[centroid][2]
            print_line = "{0},{1},t-{2}".format(community_area, centroid, days)
            for crimes in crimes_found_list: 
                print_line += ",{0}".format(crimes)
            print print_line


if __name__ == "__main__":
    source = "cent_5051.csv"
    centroid_dict = get_centroid_dict(source)
    crimes = get_crimes_list(source, centroid_dict)
    time_threshold = 15
    space_list = [600, 1200, 1800, 2400, 3000]
    make_matrix(centroid_dict, crimes, time_threshold, space_list)
