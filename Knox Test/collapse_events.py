import csv
            
def make_matrix(output_days, history_csv):

    print "beat,tract,block,days_from_end,0,600,1200,1800,2400,3000"
    
    with open(history_csv, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        crime_counter = [0,0,0,0,0,0]
        for row in crimereader:
            crime_counter[0] += int(row["0"])
            crime_counter[1] += int(row["600"])
            crime_counter[2] += int(row["1200"])
            crime_counter[3] += int(row["1800"])
            crime_counter[4] += int(row["2400"])
            crime_counter[5] += int(row["3000"])
            if int(row["days_from_end"][2:]) in output_days:
                print "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}".format(
                    row["beat"],
                    row["tract"],
                    row["block"],
                    row["days_from_end"],
                    crime_counter[0],
                    crime_counter[1],
                    crime_counter[2],
                    crime_counter[3],
                    crime_counter[4],
                    crime_counter[5])
                crime_counter = [0,0,0,0,0,0]
                    
            
    
if __name__ == "__main__":
    history_csv = "events.csv"
    output_days = [1,4,7,10,13]
    make_matrix(output_days, history_csv)
