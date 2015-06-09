
import csv

def get_knox_dict(source):

    knox_dict = {}

    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            if row[" block"] in knox_dict.keys():
                block = knox_dict[row["block"]]
                block[1] += int(row["600"]) * float(row["knox600"])
                block[2] += int(row["1200"]) * float(row["knox1200"])
                block[3] += int(row["1800"]) * float(row["knox1800"])
                block[4] += int(row["2400"]) * float(row["knox2400"])
                block[5] += int(row["3000"]) * float(row["knox3000"])
            else:
                beats = int(row["# beat"])
                six = int(row["600"]) * float(row["knox600"])
                twelve = int(row["1200"]) * float(row["knox1200"])
                eighteen = int(row["1800"]) * float(row["knox1800"])
                twentyfour = int(row["2400"]) * float(row["knox2400"])
                thirty = int(row["3000"]) * float(row["knox3000"])
                knox_dict[row["block"]] = [community_area, six, twelve, eighteen, twentyfour, thirty]
            
        return knox_dict

def make_matrix(knox_dict):

    # Header
    print "community_area,block,600ft,1200ft,1800ft,2400ft,3000ft"

    # Sort the blocks by community area
    sorted_keys = sorted(knox_dict.keys(), key=lambda x: knox_dict[x][0])

    for key in sorted_keys:
        print "{0},{1},{2},{3},{4},{5},{6}".format(knox_dict[key][0],
                                                   key,
                                                   knox_dict[key][1],
                                                   knox_dict[key][2],
                                                   knox_dict[key][3],
                                                   knox_dict[key][4],
                                                   knox_dict[key][5])

            
if __name__ == "__main__":
    knox_csv = "result.csv"
    knox_dict = get_knox_dict(knox_csv)
    make_matrix(knox_dict)
