import csv

def get_knox_dict(source):

    knox_dict = {}

    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            community_area = row["ca"]
            day = row[" time"]
            community_area = community_area[2:]
            day = str(int(day) + 1)
            iden = "{0}:{1}".format(community_area, day)
            if not iden in knox_dict.keys():
                dist600 = row[" knox600ft"]
                p600 = row[" p600ft"]
                pair600 = (dist600, p600)
                dist1200 = row[" knox1200ft"]
                p1200 = row[" p1200ft"]
                pair1200 = (dist1200, p1200)
                dist1800 = row[" knox1800ft"]
                p1800 = row[" p1800ft"]
                pair1800 = (dist1800, p1800)
                dist2400 = row[" knox2400ft"]
                p2400 = row[" p2400ft"]
                pair2400 = (dist2400, p2400)
                dist3000 = row[" knox3000ft"]
                p3000 = row[" p3000ft"]
                pair3000 = (dist3000, p3000)
                distances = (pair600, pair1200, pair1800, pair2400, pair3000)
                knox_dict[iden] = distances
                
        return knox_dict

def make_matrix(knox_dict, source):

    # crimes_dict is: "#(community_area):day" : distances
    # where distances is: (600ft, 1200ft, 1800ft, 2400ft, 3000ft)
    # That is, the knox coefficient for each

    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)

        # Header
        print "community_area,block,days_from_end,600,knox600,p-value,1200,knox1200,p-value,1800,knox1800,p-value,2400,knox2400,p-value,3000,knox3000,p-value"

        i = 0
        for row in crimereader:
            community_area = row["community_area"]
            day = row["days_from_end"]
            day = day[2:]
            iden = "{0}:{1}".format(community_area, day)
            try:
                distances = knox_dict[iden]
                print_line = ""
                print_line += community_area
                print_line += ","
                print_line += row["block"]
                print_line += ","
                print_line += row["days_from_end"]
                print_line += ","
                print_line += row["600"]
                print_line += ","
                print_line += distances[0][0]
                print_line += ","
                print_line += distances[0][1]
                print_line += ","
                print_line += row["1200"]
                print_line += ","
                print_line += distances[1][0]
                print_line += ","
                print_line += distances[1][1]
                print_line += ","
                print_line += row["1800"]
                print_line += ","
                print_line += distances[2][0]
                print_line += ","
                print_line += distances[2][1]
                print_line += ","
                print_line += row["2400"]
                print_line += ","
                print_line += distances[3][0]
                print_line += ","
                print_line += distances[3][1]
                print_line += ","
                print_line += row["3000"]
                print_line += ","
                print_line += distances[4][0]
                print_line += ","
                print_line += distances[4][1]
                print print_line
            except KeyError:
                pass

            
if __name__ == "__main__":
    event_csv = "three_day_ring_matrix_9_predictor.csv"
    knox_csv = "ringallcacorrected.csv"
    crimes_dict = get_knox_dict(knox_csv)
    make_matrix(crimes_dict, event_csv)
