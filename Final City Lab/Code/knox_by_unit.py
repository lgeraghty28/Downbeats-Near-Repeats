import shapefile
from pandas import *
import pandas as pd
from pysal.spatial_dynamics.interaction import *
import numpy
from pysal import cg
from pysal.spatial_dynamics import util
import csv

### function that makes a data frame from a  shapefile

def shp2dataframe(fname):

    shp = shapefile.Reader(fname)
    r = shp.records()
    fld = np.array(shp.fields[1:], dtype=str)
    data = pd.DataFrame(r, columns=fld[:, 0])

    return data


def modified_knox(s_coords, t_coords, delta, tau, permutations=99):

    s = s_coords
    t = t_coords
    n = len(t)

    # calculate the spatial and temporal distance matrices for the events
    sdistmat = cg.distance_matrix(s)
    tdistmat = cg.distance_matrix(t)

    # identify events within thresholds
    spacmat = np.ones((n, n))
    spacbin = sdistmat <= delta
    spacmat = spacmat * spacbin
    timemat = np.ones((n, n))
    timebin = tdistmat <= tau
    timemat = timemat * timebin

    # calculate the observed (original) statistic
    knoxmat = timemat * spacmat
    obsstat = (knoxmat.sum() - n)

    # calculate the expectated value
    ssumvec = np.reshape((spacbin.sum(axis=0) - 1), (n, 1))
    tsumvec = np.reshape((timebin.sum(axis=0) - 1), (n, 1))
    expstat = (ssumvec * tsumvec).sum()

    # calculate the modified stat
    stat = (obsstat - (expstat / (n - 1.0))) / 2.0

    # return results (if no inference)
    if not permutations:
        return stat
    distribution = []

    # loop for generating a random distribution to assess significance
    for p in range(permutations):
        rtdistmat = util.shuffle_matrix(tdistmat, range(n))
        timemat = np.ones((n, n))
        timebin = rtdistmat <= tau
        timemat = timemat * timebin

        # calculate the observed knox again
        knoxmat = timemat * spacmat
        obsstat = (knoxmat.sum() - n)

        # calculate the expectated value again
        ssumvec = np.reshape((spacbin.sum(axis=0) - 1), (n, 1))
        tsumvec = np.reshape((timebin.sum(axis=0) - 1), (n, 1))
        expstat = (ssumvec * tsumvec).sum()
        eknox   = expstat / (n - 1.0)

        # calculate the modified stat
        tempstat = (obsstat - (expstat / (n - 1.0))) / 2.0
        distribution.append(tempstat)

    # establish the pseudo significance of the observed statistic
    distribution = np.array(distribution)
    greater = np.ma.masked_greater_equal(distribution, stat)
    count = np.ma.count_masked(greater)
    pvalue = (count + 1.0) / (permutations + 1.0)

    # return results
    modknox_result = {'stat': stat, 'pvalue': pvalue,'eknox': eknox }
    return modknox_result


##read the data
sf2=shp2dataframe("../Data/chicago2010-15")

###subsetting the data...just burglaries
pd.unique(sf2['Primary_Ty'].values.ravel())
sf2 = sf2.loc[(sf2.Primary_Ty == 'BURGLARY')]
sf2 = sf2.loc[(sf2.Year==2014)]

coma = pd.unique(sf2['Community_'].values.ravel())
bl = pd.unique(sf2['Block'].values.ravel())
beat = pd.unique(sf2['Beat'].values.ravel())
trblock = pd.unique(sf2['TRACT_BLOC'].values.ravel())
ward = pd.unique(sf2['Ward'].values.ravel())


###code for beats

###to run matrix knox grouping days, its working

###tau is days, delta is time
####this includes a loop for time
##define rings of time and distance
knox  = numpy.asarray([['beat', 'time', 'knox600ft', 'knox1200ft', 'knox1800ft', 'knox2400ft', 'knox3000ft', 'p600ft', 'p1200ft', 'p1800ft', 'p2400ft', 'p3000ft']])

eknox  = numpy.asarray([['beat', 'time', 'eknox600ft', 'eknox1200ft', 'eknox1800ft', 'eknox2400ft', 'eknox3000ft', 'p600ft', 'p1200ft', 'p1800ft', 'p2400ft', 'p3000ft']])

d={}
roft = 14
rofd = 5
tau = 1
delta=600
array=[]
count=0


for x in beat:
    x = int(x)
    d["beat{0}".format(x)]=sf2.loc[(sf2.Beat == x)]
    ta = np.array(d["beat{0}".format(x)][['time_diffe']])
    ta = ta.astype(int)
    xa= np.array(d["beat{0}".format(x)]['b_x_centro'])
    ya= np.array(d["beat{0}".format(x)]['b_y_centro'])
    xa = xa.astype(float)
    ya = ya.astype(float)
    ca = np.column_stack((xa,ya))

    list = [1,4,7,10,13]

    for i in list:

        timev=int(i)
        result = modified_knox(ca, ta, delta, timev, permutations=99)
        result2 = modified_knox(ca, ta, 2*delta, timev, permutations=99)
        result3 = modified_knox(ca, ta, 3*delta, timev, permutations=99)
        result4 = modified_knox(ca, ta, 4*delta, timev, permutations=99)
        result5 = modified_knox(ca, ta, 5*delta, timev, permutations=99)

        z1 = [("beat{0}".format(x)), timev, result['stat']+result['eknox'], result2['stat']+result2['eknox'], result3['stat']+result3['eknox'], result4['stat']+result4['eknox'], result5['stat']+result5['eknox'], ("%2.8f"%result['pvalue']), ("%2.8f"%result2['pvalue']), ("%2.8f"%result3['pvalue']), ("%2.8f"%result4['pvalue']), ("%2.8f"%result5['pvalue'])]
        z2= [("beat{0}".format(x)), timev,result['eknox'], result2['eknox'], result3['eknox'], result4['eknox'], result5['eknox'],("%2.8f"%result['pvalue']), ("%2.8f"%result2['pvalue']), ("%2.8f"%result3['pvalue']), ("%2.8f"%result4['pvalue']), ("%2.8f"%result5['pvalue'])]
        knox = numpy.vstack([knox, z1])
        eknox = numpy.vstack([eknox, z2])
    count= count+1
    print (count*100.0)/len(beat), '% of beats'
    print "beat"
    print x


###make a copy of the knox array and changes the values for the values of the rings. It keeps the p values

ring = knox.copy()
for x in range(1,len(ring)):
    if np.float(ring[x][1])==1:
        try:
            ring[x][2]=np.float(knox[x][2])/np.float(eknox[x][2])
            for i in range (3,7):
                ring[x][i]= (np.float(knox[x][i])-np.float(knox[x][i-1]))/(np.float(eknox[x][i])-np.float(eknox[x][i-1]))
        except:
            pass
    else:
        try:
            ring[x][2]= (np.float(knox[x][2])-np.float(knox[x-1][2]))/(np.float(eknox[x][2])-np.float(eknox[x-1][2]))
            for i in range (3,7):
                ring[x][i]= (np.float(knox[x][i])-np.float(knox[x-1][i-1]))/(np.float(eknox[x][i])-np.float(eknox[x-1][i-1]))
        except:
            pass



#### export to csv
numpy.savetxt('knox.csv', knox, delimiter=",", fmt="%s")
numpy.savetxt('eknox.csv', eknox, delimiter=",", fmt="%s")
numpy.savetxt('ring.csv', ring, delimiter=",", fmt="%s")

