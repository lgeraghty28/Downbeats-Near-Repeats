import csv
from pandas import *
import numpy
import pandas as pd

def get_ring_dict(source):

    ring_dict = {}

    # dict["beat-day"] = [600ft knox, 1200ft knox, 1800ft knox, 2400ft knox, 3000ft knox]

    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            beat_number = row["beat"][4:]
            day_number = row["time"]
            iden = "{0}-{1}".format(beat_number, day_number)
            ring_dict[iden] = (row["knox600ft"],row["knox1200ft"],row["knox1800ft"],row["knox2400ft"],row["knox3000ft"])
        return ring_dict
            
def make_matrix(ring_dict, history_csv):

    # Header
    print "beat,block,day,tract,600ft,1200ft,1800ft,2400ft,3000ft"
    with open(history_csv, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            beat_number = row["beat"]
            day_number = row["days_from_end"][2:]
            tract_number = row["tract"]
            iden = "{0}-{1}".format(beat_number, day_number)
            if iden in ring_dict.keys():
                print "{0},{1},{2},{3},{4},{5},{6},{7},{8}".format(row["beat"],
                                                               row["block"],
                                                               row["days_from_end"][2:],
                                                               row["tract"],
                                                               float(row["600"]) * float(ring_dict[iden][0]),
                                                               float(row["1200"]) * float(ring_dict[iden][1]),
                                                               float(row["1800"]) * float(ring_dict[iden][2]),
                                                               float(row["2400"]) * float(ring_dict[iden][3]),
                                                               float(row["3000"]) * float(ring_dict[iden][4]))
                
if __name__ == "__main__":
    ring_csv = "ring.csv"
    history_csv = "3.5.collapse.events.csv"
    ring_dict = get_ring_dict(ring_csv)
    make_matrix(ring_dict, history_csv)

#d1 = pd.read_csv("coefficients.csv")

#d2 = pd.read_csv("baseline2014_tract_season.csv")
#d2=d2.rename(columns = {'Tract':'tract'})


#result = merge(d1, d2, how='inner', on=['tract'])
#result[0:]
#result['expburgs'] = (result['600ft'] + result['1200ft'] + result['1800ft'] + result['2400ft'] + result['3000ft'])*result['Jan_Mar_ave']/38
#result

#numpy.savetxt('result.csv', result, delimiter=", ", fmt="%s", header="beat,block,day,tract,600ft,1200ft,1800ft,2400ft,3000ft,Jan_Mar_ave,Apr_Jun_ave,Jul_Sep_ave,Oct_Dec_ave,expburgs")
