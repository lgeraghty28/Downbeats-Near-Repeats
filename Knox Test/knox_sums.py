import csv

def get_knox_dict(source):

    knox_dict = {}

    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            row_sum = float(row["600ft"]) + float(row["1200ft"]) + float(row["1800ft"]) + float(row["2400ft"]) + float(row["3000ft"])
            if row["block"] in knox_dict.keys():
                knox_dict[row["block"]][2] += row_sum
            else:
                knox_dict[row["block"]] = [row["beat"],row["tract"], row_sum]

    return knox_dict

def make_matrix(input_dict):

    print_line = "beat,block,tract,knox_sum\n"
    
    for key in input_dict.keys():
        print_line += "{0},{1},{2},{3}\n".format(input_dict[key][0],
                                               key,
                                               input_dict[key][1],
                                               input_dict[key][2])

    with open("knox_sums.csv", "w") as csvfile:
        csvfile.write(print_line)

d5 = get_knox_dict('3.24.coefficients.csv')
make_matrix(d5)

if __name__ == "__main__":
    knox_csv = "result.csv"
    knox_dict = get_knox_dict(knox_csv)
    make_matrix(knox_dict)
