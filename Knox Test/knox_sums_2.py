#sum knox coefficients to get "score" for each block

import shapefile
from pandas import *
import pandas as pd
from pysal.spatial_dynamics.interaction import *
import numpy
from pysal import cg
from pysal.spatial_dynamics import util
import csv

def get_knox_dict(source):

    knox_dict = {}

    with open(source, "rU") as csvfile:
        crimereader = csv.DictReader(csvfile)
        for row in crimereader:
            row_sum = float(row["600ft"]) + float(row["1200ft"])# + float(row["1800ft"]) + float(row["2400ft"]) + float(row["3000ft"])
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

d5 = get_knox_dict('3.5.coefficients.csv')
make_matrix(d5)



d1 = pd.read_csv("knox_sums.csv")
#d1 = pd.pivot_table(d1,index=["block","beat","tract"], aggfunc=np.sum)
d2 = pd.read_csv("baseline2014_tract_season.csv")



result = merge(d1, d2, how='inner', on=['tract'])
result['expburgs'] = (result['knox_sum'] )*result['Jan_Mar_ave']/38
result['baseline']= result['Jan_Mar_ave']/38

result

numpy.savetxt('result.csv', result, delimiter=", ", fmt="%s", header="beat,block,tract,knox_sums,Jan_Mar_ave,Apr_Jun_ave,Jul_Sep_ave,Oct_Dec_ave,expburgs,baseline")
