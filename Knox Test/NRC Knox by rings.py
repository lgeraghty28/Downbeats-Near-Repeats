####AGC
# coding: utf-8

# In[2]:

import shapefile
import numpy as np
from pandas import *
#import geopandas
#import pandashp as pdshp
import pylab


# In[3]:

import pandas as pd
from prettytable import PrettyTable


# In[4]:

###choose the place where the files are
import os
os.getcwd()


os.chdir("C:/Users/titog/Desktop/city lab/final files/")


# In[5]:

### function that makes a data frame from a  shapefile 

def shp2dataframe(fname):


    shp = shapefile.Reader(fname)

    r = shp.records()

    fld = np.array(shp.fields[1:], dtype=str)

    data = pd.DataFrame(r, columns=fld[:, 0])

    del shp

    return data


# In[6]:

##read the data
sf2=shp2dataframe("C:/Users/titog/Desktop/city lab/final files/chicago2010-15")


# In[7]:

###check that the data is read
sf2.head()


# In[8]:

###ame of the variables

list(sf2.columns.values)


# In[9]:

###subsetting the data...just burgs
sf2['Primary_Ty'] 
pd.unique(sf2['Primary_Ty'].values.ravel())
sf2 = sf2.loc[(sf2.Primary_Ty == 'BURGLARY')]
len(sf2['Primary_Ty'] )


# In[12]:

coma = pd.unique(sf2['Community_'].values.ravel())
bl = pd.unique(sf2['Block'].values.ravel())
beat = pd.unique(sf2['Beat'].values.ravel())
trblock = pd.unique(sf2['TRACT_BLOC'].values.ravel())
ward = pd.unique(sf2['Ward'].values.ravel())


# In[ ]:

#####paysal code


"""
Methods for identifying space-time interaction in spatio-temporal event
data.

"""
__author__ = "Nicholas Malizia <nmalizia@asu.edu>", "Sergio J. Rey <srey@asu.edu>", "Philip Stephens <philip.stephens@asu.edu"

__all__ = ['SpaceTimeEvents', 'knox', 'mantel', 'jacquez', 'modified_knox']

import pysal
import numpy as np
import scipy.stats as stats
import pysal.weights.Distance as Distance
from pysal import cg
from pysal.spatial_dynamics import util
from datetime import date

class SpaceTimeEvents:
    """
    Method for reformatting event data stored in a shapefile for use in
    calculating metrics of spatio-temporal interaction.

    Parameters
    ----------
    path            : string
                      the path to the appropriate shapefile, including the
                      file name, but excluding the extension.
    time            : string
                      column header in the DBF file indicating the column
                      containing the time stamp.
    infer_timestamp : bool, optional
                      if the column containing the timestamp is formatted as
                      calendar dates, try to coerce them into Python datetime 
                      objects (the default is False).

    Attributes
    ----------
    n               : int
                      number of events.
    x               : array
                      (n, 1), array of the x coordinates for the events.
    y               : array
                      (n, 1), array of the y coordinates for the events.
    t               : array
                      (n, 1), array of the temporal coordinates for the events.
    space           : array
                      (n, 1), array of the spatial coordinates (x,y) for the
                      events.
    time            : array
                      (n, 1), array of the temporal coordinates (t,1) for the
                      events, the second column is a vector of ones.

    Examples
    --------
    Read in the example shapefile data, ensuring to omit the file
    extension. In order to successfully create the event data the .dbf file
    associated with the shapefile should have a column of values that are a
    timestamp for the events. This timestamp may be a numerical value
    or a date. Date inference was added in version 1.6.

    >>> path = pysal.examples.get_path("burkitt")

    Create an instance of SpaceTimeEvents from a shapefile, where the
    temporal information is stored in a column named "T".

    >>> events = SpaceTimeEvents(path,'T')

    See how many events are in the instance.

    >>> events.n
    188

    Check the spatial coordinates of the first event.

    >>> events.space[0]
    array([ 300.,  302.])

    Check the time of the first event.

    >>> events.t[0]
    array([ 413.])

    Calculate the time difference between the first two events.

    >>> events.t[1] - events.t[0]
    array([ 59.])

    New, in 1.6, date support:

    Now, create an instance of SpaceTimeEvents from a shapefile, where the
    temporal information is stored in a column named "DATE".

    >>> events = SpaceTimeEvents(path,'DATE')

    See how many events are in the instance.

    >>> events.n
    188

    Check the spatial coordinates of the first event.

    >>> events.space[0]
    array([ 300.,  302.])

    Check the time of the first event. Note that this value is equivalent to
    413 days after January 1, 1900.

    >>> events.t[0][0]
    datetime.date(1901, 2, 16)

    Calculate the time difference between the first two events.

    >>> (events.t[1][0] - events.t[0][0]).days
    59

    """
    def __init__(self, path, time_col, infer_timestamp=False):
        shp = pysal.open(path + '.shp')
        dbf = pysal.open(path + '.dbf')

        # extract the spatial coordinates from the shapefile
        x = [coords[0] for coords in shp]
        y = [coords[1] for coords in shp]

        self.n = n = len(shp)
        x = np.array(x)
        y = np.array(y)
        self.x = np.reshape(x, (n, 1))
        self.y = np.reshape(y, (n, 1))
        self.space = np.hstack((self.x, self.y))

        # extract the temporal information from the database
        if infer_timestamp:
            col = dbf.by_col(time_col)
            if isinstance(col[0], date):
                day1 = min(col)
                col = [(d - day1).days for d in col]
                t = np.array(col)
            else:
                print("Unable to parse your time column as Python datetime                       objects, proceeding as integers.")
                t = np.array(col)
        else:
            t = np.array(dbf.by_col(time_col))
        line = np.ones((n, 1))
        self.t = np.reshape(t, (n, 1))
        self.time = np.hstack((self.t, line))

        # close open objects
        dbf.close()
        shp.close()


def knox(s_coords, t_coords, delta, tau, permutations=99, debug=False):
    """
    Knox test for spatio-temporal interaction. [1]_

    Parameters
    ----------
    s_coords        : array
                      (n, 2), spatial coordinates.
    t_coords        : array
                      (n, 1), temporal coordinates.
    delta           : float
                      threshold for proximity in space.
    tau             : float
                      threshold for proximity in time.
    permutations    : int, optional
                      the number of permutations used to establish pseudo-
                      significance (the default is 99).
    debug           : bool, optional
                      if true, debugging information is printed (the default is 
                      False).

    Returns
    -------
    knox_result     : dictionary
                      contains the statistic (stat) for the test and the
                      associated p-value (pvalue).
    stat            : float
                      value of the knox test for the dataset.
    pvalue          : float
                      pseudo p-value associated with the statistic.
    counts          : int
                      count of space time neighbors.

    References
    ----------
    .. [1] E. Knox. 1964. The detection of space-time
       interactions. Journal of the Royal Statistical Society. Series C
       (Applied Statistics), 13(1):25-30.

    Examples
    --------
    >>> import numpy as np
    >>> import pysal

    Read in the example data and create an instance of SpaceTimeEvents.

    >>> path = pysal.examples.get_path("burkitt")
    >>> events = SpaceTimeEvents(path,'T')

    Set the random seed generator. This is used by the permutation based
    inference to replicate the pseudo-significance of our example results -
    the end-user will normally omit this step.

    >>> np.random.seed(100)

    Run the Knox test with distance and time thresholds of 20 and 5,
    respectively. This counts the events that are closer than 20 units in
    space, and 5 units in time.

    >>> result = knox(events.space, events.t, delta=20, tau=5, permutations=99)

    Next, we examine the results. First, we call the statistic from the
    results dictionary. This reports that there are 13 events close
    in both space and time, according to our threshold definitions.

    >>> result['stat'] == 13
    True

    Next, we look at the pseudo-significance of this value, calculated by
    permuting the timestamps and rerunning the statistics. In this case,
    the results indicate there is likely no space-time interaction between
    the events.

    >>> print("%2.2f"%result['pvalue'])
    0.17

    """

    # Do a kdtree on space first as the number of ties (identical points) is
    # likely to be lower for space than time.

    kd_s = pysal.cg.KDTree(s_coords)
    neigh_s = kd_s.query_pairs(delta)
    tau2 = tau * tau
    ids = np.array(list(neigh_s))

    # For the neighboring pairs in space, determine which are also time
    # neighbors

    d_t = (t_coords[ids[:, 0]] - t_coords[ids[:, 1]]) ** 2
    n_st = sum(d_t <= tau2)

    knox_result = {'stat': n_st[0]}

    if permutations:
        joint = np.zeros((permutations, 1), int)
        for p in xrange(permutations):
            np.random.shuffle(t_coords)
            d_t = (t_coords[ids[:, 0]] - t_coords[ids[:, 1]]) ** 2
            joint[p] = np.sum(d_t <= tau2)

        larger = sum(joint >= n_st[0])
        if (permutations - larger) < larger:
            larger = permutations - larger
        p_sim = (larger + 1.) / (permutations + 1.)
        knox_result['pvalue'] = p_sim
    return knox_result


def mantel(s_coords, t_coords, permutations=99, scon=1.0, spow=-1.0, tcon=1.0, tpow=-1.0):
    """
    Standardized Mantel test for spatio-temporal interaction. [2]_

    Parameters
    ----------
    s_coords        : array
                      (n, 2), spatial coordinates.
    t_coords        : array
                      (n, 1), temporal coordinates.
    permutations    : int, optional
                      the number of permutations used to establish pseudo-
                      significance (the default is 99).
    scon            : float, optional
                      constant added to spatial distances (the default is 1.0).
    spow            : float, optional
                      value for power transformation for spatial distances 
                      (the default is -1.0).
    tcon            : float, optional
                      constant added to temporal distances (the default is 1.0).
    tpow            : float, optional
                      value for power transformation for temporal distances 
                      (the default is -1.0).

    Returns
    -------
    mantel_result   : dictionary
                      contains the statistic (stat) for the test and the
                      associated p-value (pvalue).
    stat            : float
                      value of the knox test for the dataset.
    pvalue          : float
                      pseudo p-value associated with the statistic.

    References
    ----------
    .. [2] N. Mantel. 1967. The detection of disease clustering and a
       generalized regression approach. Cancer Research, 27(2):209-220.

    Examples
    --------
    >>> import numpy as np
    >>> import pysal

    Read in the example data and create an instance of SpaceTimeEvents.

    >>> path = pysal.examples.get_path("burkitt")
    >>> events = SpaceTimeEvents(path,'T')

    Set the random seed generator. This is used by the permutation based
    inference to replicate the pseudo-significance of our example results -
    the end-user will normally omit this step.

    >>> np.random.seed(100)

    The standardized Mantel test is a measure of matrix correlation between
    the spatial and temporal distance matrices of the event dataset. The
    following example runs the standardized Mantel test without a constant
    or transformation; however, as recommended by Mantel (1967) [2]_, these
    should be added by the user. This can be done by adjusting the constant
    and power parameters.

    >>> result = mantel(events.space, events.t, 99, scon=1.0, spow=-1.0, tcon=1.0, tpow=-1.0)

    Next, we examine the result of the test.

    >>> print("%6.6f"%result['stat'])
    0.048368

    Finally, we look at the pseudo-significance of this value, calculated by
    permuting the timestamps and rerunning the statistic for each of the 99
    permutations. According to these parameters, the results indicate
    space-time interaction between the events.

    >>> print("%2.2f"%result['pvalue'])
    0.01

    """

    t = t_coords
    s = s_coords
    n = len(t)

    # calculate the spatial and temporal distance matrices for the events
    distmat = cg.distance_matrix(s)
    timemat = cg.distance_matrix(t)

    # calculate the transformed standardized statistic
    timevec = (util.get_lower(timemat) + tcon) ** tpow
    distvec = (util.get_lower(distmat) + scon) ** spow
    stat = stats.pearsonr(timevec, distvec)[0].sum()

    # return the results (if no inference)
    if not permutations:
        return stat

    # loop for generating a random distribution to assess significance
    dist = []
    for i in range(permutations):
        trand = util.shuffle_matrix(timemat, range(n))
        timevec = (util.get_lower(trand) + tcon) ** tpow
        m = stats.pearsonr(timevec, distvec)[0].sum()
        dist.append(m)

    ## establish the pseudo significance of the observed statistic
    distribution = np.array(dist)
    greater = np.ma.masked_greater_equal(distribution, stat)
    count = np.ma.count_masked(greater)
    pvalue = (count + 1.0) / (permutations + 1.0)

    # report the results
    mantel_result = {'stat': stat, 'pvalue': pvalue}
    return mantel_result


def jacquez(s_coords, t_coords, k, permutations=99):
    """
    Jacquez k nearest neighbors test for spatio-temporal interaction. [3]_

    Parameters
    ----------
    s_coords        : array
                      (n, 2), spatial coordinates.
    t_coords        : array
                      (n, 1), temporal coordinates.
    k               : int
                      the number of nearest neighbors to be searched.
    permutations    : int, optional
                      the number of permutations used to establish pseudo-
                      significance (the default is 99).

    Returns
    -------
    jacquez_result  : dictionary
                      contains the statistic (stat) for the test and the
                      associated p-value (pvalue).
    stat            : float
                      value of the Jacquez k nearest neighbors test for the
                      dataset.
    pvalue          : float
                      p-value associated with the statistic (normally
                      distributed with k-1 df).

    References
    ----------
    .. [3] G. Jacquez. 1996. A k nearest neighbour test for space-time
       interaction. Statistics in Medicine, 15(18):1935-1949.

    Examples
    --------
    >>> import numpy as np
    >>> import pysal

    Read in the example data and create an instance of SpaceTimeEvents.

    >>> path = pysal.examples.get_path("burkitt")
    >>> events = SpaceTimeEvents(path,'T')

    The Jacquez test counts the number of events that are k nearest
    neighbors in both time and space. The following runs the Jacquez test
    on the example data and reports the resulting statistic. In this case,
    there are 13 instances where events are nearest neighbors in both space
    and time.

    # turning off as kdtree changes from scipy < 0.12 return 13
    #>>> np.random.seed(100)
    #>>> result = jacquez(events.space, events.t ,k=3,permutations=99)
    #>>> print result['stat']
    #12

    The significance of this can be assessed by calling the p-
    value from the results dictionary, as shown below. Again, no
    space-time interaction is observed.

    #>>> result['pvalue'] < 0.01
    #False

    """
    time = t_coords
    space = s_coords
    n = len(time)

    # calculate the nearest neighbors in space and time separately
    knnt = Distance.knnW(time, k)
    knns = Distance.knnW(space, k)

    nnt = knnt.neighbors
    nns = knns.neighbors
    knn_sum = 0

    # determine which events are nearest neighbors in both space and time
    for i in range(n):
        t_neighbors = nnt[i]
        s_neighbors = nns[i]
        check = set(t_neighbors)
        inter = check.intersection(s_neighbors)
        count = len(inter)
        knn_sum += count

    stat = knn_sum

    # return the results (if no inference)
    if not permutations:
        return stat

    # loop for generating a random distribution to assess significance
    dist = []
    for p in range(permutations):
        j = 0
        trand = np.random.permutation(time)
        knnt = Distance.knnW(trand, k)
        nnt = knnt.neighbors
        for i in range(n):
            t_neighbors = nnt[i]
            s_neighbors = nns[i]
            check = set(t_neighbors)
            inter = check.intersection(s_neighbors)
            count = len(inter)
            j += count

        dist.append(j)

    # establish the pseudo significance of the observed statistic
    distribution = np.array(dist)
    greater = np.ma.masked_greater_equal(distribution, stat)
    count = np.ma.count_masked(greater)
    pvalue = (count + 1.0) / (permutations + 1.0)

    # report the results
    jacquez_result = {'stat': stat, 'pvalue': pvalue}
    return jacquez_result


def modified_knox(s_coords, t_coords, delta, tau, permutations=99):
    """
    Baker's modified Knox test for spatio-temporal interaction. [4]_

    Parameters
    ----------
    s_coords        : array
                      (n, 2), spatial coordinates.
    t_coords        : array
                      (n, 1), temporal coordinates.
    delta           : float
                      threshold for proximity in space.
    tau             : float
                      threshold for proximity in time.
    permutations    : int, optional
                      the number of permutations used to establish pseudo-
                      significance (the default is 99).

    Returns
    -------
    modknox_result  : dictionary
                      contains the statistic (stat) for the test and the
                      associated p-value (pvalue).
    stat            : float
                      value of the modified knox test for the dataset.
    pvalue          : float
                      pseudo p-value associated with the statistic.

    References
    ----------
    .. [4] R.D. Baker. Identifying space-time disease clusters. Acta Tropica,
       91(3):291-299, 2004.

    Examples
    --------
    >>> import numpy as np
    >>> import pysal

    Read in the example data and create an instance of SpaceTimeEvents.

    >>> path = pysal.examples.get_path("burkitt")
    >>> events = SpaceTimeEvents(path, 'T')

    Set the random seed generator. This is used by the permutation based
    inference to replicate the pseudo-significance of our example results -
    the end-user will normally omit this step.

    >>> np.random.seed(100)

    Run the modified Knox test with distance and time thresholds of 20 and 5,
    respectively. This counts the events that are closer than 20 units in
    space, and 5 units in time.

    >>> result = modified_knox(events.space, events.t, delta=20, tau=5, permutations=99)

    Next, we examine the results. First, we call the statistic from the
    results dictionary. This reports the difference between the observed
    and expected Knox statistic.

    >>> print("%2.8f" % result['stat'])
    2.81016043

    Next, we look at the pseudo-significance of this value, calculated by
    permuting the timestamps and rerunning the statistics. In this case,
    the results indicate there is likely no space-time interaction.

    >>> print("%2.2f" % result['pvalue'])
    0.11

    """
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()


# In[ ]:

###to run matrix knox grouping days, its working

###tau is days, delta is time
####this includes a loop for time
##define rings of time and distance
import numpy
#knox  = numpy.asarray([['ca', 'time', 'knox600ft', 'knox1200ft', 'knox1800ft', 'knox2400ft', 'knox3000ft', 'p600ft', 'p1200ft', 'p1800ft', 'p2400ft', 'p3000ft', 'exknox600', 'exknox1200', 'exknox1800', 'exknox2400', 'exknox3000' ]])
knox  = numpy.asarray([['ca', 'time', 'knox600ft', 'knox1200ft', 'knox1800ft', 'knox2400ft', 'knox3000ft', 'p600ft', 'p1200ft', 'p1800ft', 'p2400ft', 'p3000ft']])


eknox  = numpy.asarray([['ca', 'time', 'eknox600ft', 'eknox1200ft', 'eknox1800ft', 'eknox2400ft', 'eknox3000ft', 'p600ft', 'p1200ft', 'p1800ft', 'p2400ft', 'p3000ft']])

d={}
roft = 14
rofd = 5
tau = 1
delta=600
array=[]
count=0

##### list of days rings you want to get
list = [1,4,7,10,13]
  
### here you can use blocks or community areas replacing  range(25,78)   by coma as example 
    
for x in coma:
    d["ca{0}".format(x)]=sf2.loc[(sf2.Community_ == x)]
    ta = np.array(d["ca{0}".format(x)][['time_diffe']])
    ta = ta.astype(int)
    xa= np.array(d["ca{0}".format(x)]['b_x_centro'])
    ya= np.array(d["ca{0}".format(x)]['b_y_centro'])
    xa = ta.astype(int)
    ya = ta.astype(int)
    #ta = np.array(d["ca{0}".format(x)]['time'])
    #xa= np.array(d["ca{0}".format(x)]['X_Coordina'])
    #ya= np.array(d["ca{0}".format(x)]['Y_Coordina'])
    largo = len(ta)
    #sc = np.array(sf2)
    ca = np.column_stack((xa,ya))
    
    
    
    
    
    for i in list:
        
        
        timev=int(i)
                           
        result = modified_knox(ca, ta, delta, timev, permutations=99)
        result2 = modified_knox(ca, ta, 2*delta, timev, permutations=99)
        result3 = modified_knox(ca, ta, 3*delta, timev, permutations=99)
        result4 = modified_knox(ca, ta, 4*delta, timev, permutations=99)
        result5 = modified_knox(ca, ta, 5*delta, timev, permutations=99)
        
        
        ####Knox over eknox ...not being used in rings
        #ststat = str((result['stat']+result['eknox'])*1.0/(result['eknox']))
        #ststat2 = str((result2['stat']+result2['eknox'])*1.0/(result2['eknox']))
        #ststat3 = str((result3['stat']+result3['eknox'])*1.0/(result3['eknox']))
        #ststat4 = str((result4['stat']+result4['eknox'])*1.0/(result4['eknox']))
        #ststat5 = str((result5['stat']+result5['eknox'])*1.0/(result5['eknox']))
        
        z1 = [("ca{0}".format(x)), timev, result['stat']+result['eknox'], result2['stat']+result2['eknox'], result3['stat']+result3['eknox'], result4['stat']+result4['eknox'], result5['stat']+result5['eknox'], ("%2.8f"%result['pvalue']), ("%2.8f"%result2['pvalue']), ("%2.8f"%result3['pvalue']), ("%2.8f"%result4['pvalue']), ("%2.8f"%result5['pvalue'])]
        z2= [("ca{0}".format(x)), timev,result['eknox'], result2['eknox'], result3['eknox'], result4['eknox'], result5['eknox'],("%2.8f"%result['pvalue']), ("%2.8f"%result2['pvalue']), ("%2.8f"%result3['pvalue']), ("%2.8f"%result4['pvalue']), ("%2.8f"%result5['pvalue'])]
        #arknox = numpy.vstack([arknox, z])
        knox = numpy.vstack([knox, z1])
        eknox = numpy.vstack([eknox, z2])
        print "ring"
        print i
        #print z1, z2
    count= count+1
    #print (count*100.0)/len(coma), '% of the ca'
    print "ca"
    print x
    d={}
    #print largo
  # 

#knox


# In[ ]:

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
#a=np.float(knox [1][2])
#np.float(knox[1][2])-np.float(eknox[1][2])
ring


# In[ ]:

#### export to csv

eknox
os.chdir("C:/Users/titog/Desktop/city lab/final files/")
numpy.savetxt('knox.csv', knox, delimiter=", ", fmt="%s")
numpy.savetxt('eknox.csv', eknox, delimiter=", ", fmt="%s")
numpy.savetxt('ring.csv', ring, delimiter=", ", fmt="%s")

