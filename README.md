<h1>Introduction and overview to our "near-repeat" analysis of burglaries in the Chicago crime data</h1>
<p>This is our exploration of the "near-repeat" phenomenon in burglaries in the city of <a href="https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2">Chicago's crime data portal</a>, which contains information on all reported crimes from 2001-present. "Near-repeat" patterns in crime occurrences refer to an increased probability of a type of crime happening in close spatial and temporal proximity to a previous crime.  This code and analysis are the beginning of a tool that might help Chicago police become more efficient in how they allocate law enforcement resources by identifying areas that are the most likely to have a crime on a particular day based on the recent history of crime in that area.</p>
<p>Our documentation in this repo includes our methodology for using the knox test in Chicago crime data, information on the knox test for space-time analysis, which was the method we used in our investigation, and instructions on how to use the data and code included in our repository. Additionally, we have included an outline of next steps for improved space-time analysis to be used in future near-repeat analysis of Chicago crime data.</p>
<h1>Instructions on how to use this repo to generate knox scores and expected values of burglaries</h1>
<h3>I. Context on Near-repeat analysis & Knox Method</h3>
<p><a href="http://www.math.ucla.edu/~mbshort/papers/crime2.pdf">Evidence in the literature</a> on crime prediction suggests that "near-repeat" analysis, or measuring the increased tendency for crimes to occur within a certain time and spatial proximity of a previous crime, may be a way to make law enforcement allocation more efficient. Near-repeat analysis might be used to determine where extra police resources are allocated throughout a particular district or police beat to maximize the likelihood that police officers will be able to prevent a crime from taking place. </p>
<p>In our analysis, we used the <a href="http://www.spatial.cs.umn.edu/Courses/Fall07/8715/papers/kuldorff_hjalmars.pdf">Knox method</a> for space-time analysis. The Knox test is one of a number of statistical tests to examine space-time clustering, or whether the clustering of a group of events in a particular time and place is statistically significant. The Knox test, <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1058931/">first developed</a> by epidemiologist George Knox 1964 to study childhood leukemia, examines whether a clustering of events is significantly different from a random distribution. In crime analysis, this test has been implemented by the <a href="http://www.cla.temple.edu/cj/misc/nr/">Near-Repeat calculator</a> developed by researchers at Temple University, which allows users to enter historical burglary data into an interface and, based on the historical information, get a coefficient of the increased likelihood of a burglary occurring in particular spatial and time parameters. For example, a coefficient of 1.7 at 600 feet and one day in a particular area means that a burglary is 1.7 times more likely than usual to occur in that area given a crime occurrence the day before.</p>
<p>The Knox method is just one approach to define spatio-temporal clusters. Generally, spatial cluster detection differs from simple cluster detection in that it finds regions where some quantity is significantly higher than expected, adjusting for the underlying population or baseline. Cluster detection simply groups data points and identifies areas with a high frequency.</p>
<p>Spatial cluster detection is also different from anomaly detection. Anomaly detection focuses on single data points to determine whether or not those points are normal given the data set. Spatial cluster detection focuses on finding anomalous spatial groups or patterns. In essence, it tries to identify the locations, shapes, sizes, and other parameters of potential clusters by testing the null hypothesis, which is that there are no clusters vs. the alternative hypothesis, where each set represents a cluster in some region. Detection focuses on use areas with an abnormally high number of occurrences of use symptoms, or proxy variables (such as OTC medicine purchase, 911 calls, school and work absenteeism) to find anomalous patterns. Another key component of this type of analysis is that timely detection must be achieved while keeping the number of false alarms to a minimum, or to determine whether each of these anomalous regions is due to a genuine and relevant cluster, or simply a chance occurrence. If the relations are statistically significant can be estimated with a P-value, posterior probability, or by testing to tell which are likely to be "true" clusters and which are likely to have occurred by chance.</p>
<h3>II. Software requirements to run the Knox near repeat analysis</h3>
<p>The following software and packages are required to  run the Knox program:</p>
<ul>
<li><a href="https://www.python.org/downloads/">Python version 2</a> with <a href="https://pysal.readthedocs.org/en/latest/">PySal</a>, <a href="http://www.numpy.org/">NumPy</a>, <a href="http://www.scipy.org/">SciPy</a>, <a href="http://pandas.pydata.org/">Pandas</a>, <a href="https://code.google.com/p/prettytable/">PrettyTable</a>, <a href="https://code.google.com/p/pyshp/">PyShp</a>, <a href="http://wiki.scipy.org/PyLab">PyLab</a>, and <a href="https://docs.python.org/2/library/csv.html">csv</a>.</li>
<li><a href="http://www.r-project.org/">R version 3</a> or RStudio with <a href="http://www.r-project.org/">‘lubridate'</a> package to process dates.</li>
<li>ArcGIS (to generate the Shapefile) </li>
</ul>
<h3>III. How to run the Knox near repeat analysis</h3>
<ol>
<li><h5>Directory folder:</h5><p>generate a folder that contains the following input files, which can be found in the Final -> Data folder:</p>
<ul>
<li><h5>Crimes database:</h5> <p>In order to conduct the Knox analysis for burglaries in Chicago, we used the <a href="https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2">City of Chicago Data Portal</a> Crimes dataset. It contains information on crime from 2001 to present. We had 339,778 observations classified by the primary type of crime, primary type, description, location (jittered by block). In Chicago, there are 37,575 blocks, 300 beats, 77 community areas, 50 wards, and 21 districts. We have the date information with day, year, month and hour of occurrence of the crime. We created a comma separated values (csv) file with information on Chicago burglaries information from 2010-to date. The entire file can be downloaded directly from the City of Chicago data portal, but we have included a compressed csv with burglaries from 2010-15 in our repo.</p></li>
<li><h5>Shapefile: </h5><p>Shapefiles with burglary case points merged with census tract and census block boundaries, and census block centroids xy coordinates. The original crime data we downloaded from the city data portal is lacking geographic information on census tracts and census blocks, but they include xy coordinates that can be used to locate tracts and blocks in the Chicago shapefiles. So through ArcGIS, we successfully assigned burglary case points to census tracts and census blocks polygons.To generated the geographic centroids of census blocks in the form of xy coordinates, we created new columns of variables in shapefile attribute table, with "geo calculator", we obtain the xy centroid coordinate values, which should the the mean of the range of x coordinates of the polygon boundaries, and the mean of the range of y coordinate of the boundaries.  The original boundary shapefile can also be downloaded through city data portal. For 2010 census tract : https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Tracts-2010/5jrd-6zik  For 2010 census block: https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Blocks-2010/mfzt-js4n </p></li>
<li><h5>Crime baseline file: </h5><p>Baseline csv file, which contains a average daily baseline of burglaries for each census tract in Chicago in 2014 and included in our repo (processed in R). </p></item>
</ul>
<li><h5>Run the Knox analysis program (shell script), which can be found in the City Lab Final -> Code folder:</h5><p>In order to run the code, first you will have to clone the repository, specify the new working directory as well as install the packages mentioned in the requirements part of this document. You will find the Python Knox analysis program in the "Final-> Code" github folder. Then, you can run the shell script "Knox_shell.sh" in the code folder to get an output file that contains the knox "score" for each census block. This output file includes both a sum of the estimated coefficients for the specified time and space proximities and an expected value of burglaries for each census block, which multiplies the score by the baseline probability of a burglary occurring in each census block in that month.</p></li>
</ol>
<h3>V. Methodology</h3>
<p>We developed a methodology that allows us to compare different geographical areas in terms of the expected marginal increase in burglaries for the next day, taking into account the baseline of burglaries for each region. Our approach is as follows:</p>
<ol>
<li><h5>Define block centroid for each burglary observation: </h5><p>We decided to use the centroid of the census block for each of the crimes instead of the  X and Y coordinates that appear in the City of Chicago database. It is important to note that the geographic information for each crime provided by the City of Chicago is jittered. Each time there is a crime the police department registers that event randomly in the block where the event occurred for privacy reasons. However, in some areas, the data suggests that the same place is being assigned with a higher frequency for the same day. The latter can impact the efficiency of the knox estimation. To analyze this, we examined burglaries that happened the same day in Archer Heights, North Center, and Portage Park community areas and found that 58% of the observations had the same X and Y coordinates. To solve this, the coordinates in the crime data portal are replaced by the coordinates of the centroids of each census block.</p></li>
<li><h5>Estimate Knox Matrix for each geographic region: </h5><p>    Choosing the right geographic unit is about searching for a balance between standard error and precision in terms of time and space. We want precise estimates, but if we disaggregate time and/or space too much, we increase the Knox test's standard error (or the analysis simply does not run).The Knox analysis is more robust in larger geographic areas areas. If there are no crimes in a certain area or if the expected knox coefficient is zero, it's not possible to get an estimate of the coefficient. That is the reason why we chose to use beats as a region to estimate Knox coefficient. Beats are the smallest possible geographic segmentation of the city where it is still possible to get significant coefficients. </p>
<p>Additionally, the analysis is done using data from the 2014. There has been an important decrease in the number of burglaries in the last 2 years with respect to past data, so 2014 is a more accurate source of information for predicting future years than using previous years. The coefficients are calculated in the same way as the <a href="http://www.cla.temple.edu/cj/misc/nr/">Near Repeat Calculator</a> from Temple University using euclidean distances. Its coefficients are the  observed Knox divided by the expected Knox. The first one count all the events that meet the requirements used as inputs and the second one is how many events you would expect to happen in that spatio temporal range. Thus, the coefficient can be interpreted as the increased probability of having a new crime increases given that there was a crime in the spatio temporal range defined. Finally, the coefficients are calculated for rings using as time thresholds from 0 to 1,  4,  7, 10 and 13 days and as spatial thresholds 600 ft, 1200 ft , 1800 ft, 2400 ft and 3000 ft. We extrapolate the knox score value from the beat to the block to calculated the expected value of burglaries for each block.</li>
<li><h5>Time-distance matrix with burglaries information for each geographic region: </h5><p>For each block, we count the number of burglaries that happened for the same spatio temporal segments used to calculate the knox coefficients using the distance between centroids as the spatial distance. </p></li>
<li><h5>Multiply Knox Matrix by Time-distance Matrix and by the census tracts baseline: </h5><p>Chicago has 877 census tracts, 281 beats, and over 30,000 census blocks. Census tracts have on average 38 blocks and they are the smallest available geographic unit of analysis that we could use to get a stable baseline. To get the expected value of the number of burglaries happening on each block for each day, we multiplied the knox score, or the sum of the knox coefficient for all spatial and temporal parameters by the sum of burglaries that happened on the corresponding day by the baseline probability of a burglary occurring in a given area.</p></li>
<li><h5>Baseline by seasons: </h5><p>Our baseline are the average daily burglary counts by Chicago census tracts in seasonal quarters in 2014. January to March is season 1, April to June as season 2, July to September is season 3 and October to December is season 4. We are taking the total burglary counts per tract per season, and divide the value by 90 days to obtain the average counts. In our early descriptive analysis, we found that burglaries had a seasonal fluctuation and thus we think it is a good idea to capture the seasonality by seasonal average instead of yearly average. We also tried monthly average daily counts, but that approach produces large amount of zero outcomes that will offset knox influence, so we decided to expand our baseline to 2014 seasonal quarters. </p></li> 
<li><h5>Rank the blocks by score: </h5><p>To get the expected number of crimes, we multiply the knox coefficient by the burglary count for the same range of time and space. Then, we add all those coefficients which is interpreted as the relative heightened probability of having a crime the day after given the history of crimes in the recent days and close areas. Finally, we multiply that number by the baseline to get the expected value of burglaries on a given census block on a particular day.</p></li>
</ol>
<h3>Results and comparisons of predicted and actual burglaries in the city of Chicago  </h5>
<p>We compared the knox scores for several days in the month of March to the observed burglaries using knox coefficients calculated by Chicago police beat and Chicago community areas. In general, we found a high concentration of observed burglaries based on the predicted expected value. The highest predicted scores correlated, or those above the 98th percentile, corresponded with 15% -  30% among of the burglaries that actually occurred the next day, and 30% to 45% of the observed burglaries on the next day corresponded with expected values above the 95th percentile. Examples in the results folder demonstrate some of these results. Based on this analysis, we recommend that police departments interested in using the Knox test to make allocation more efficient focus on the blocks with the highest 2% of the predicted expected values. Further analysis and work on this topic suggests that focusing on these blocks might mean avoiding around the 20% of the burglaries concentrated in 600 blocks in close spatial and temporal proximity.</p>
<h3>VII. Other approaches to near-repeat analysis with space-time econometrics & next steps to continue this work</h3>
<p>The Knox method is just one way of approaching near-repeat analysis. We were not able to explore a modified version of the Knox in this project, but those who are interested in exploring near-repeat analysis might benefit from the following literature review:</p>
<p>The literature of Detection of Spatio-Temporal clusters is clearly explained by Daniel B. Neill in his Ph.D. thesis: Detection of spatial and spatio-temporal clusters. Daniel is Associate Professor of Information Systems in the Heinz College at Carnegie Mellon, Carnegie Mellon University.  He is also the Director of the Event and Pattern Detection Laboratory. He has conducted work on Disease Surveillance, Health Care, Fast Generalized Subset Scanning, Law Enforcement and Urban Analytics, and Learning Event Models. The objective of his work is aligned with the purpose of our study: automatically detect regions of space that are "anomalous," "unexpected," or otherwise "interesting." Finding regions of space where the values of some quantity (the "count") are significantly higher than expected, given some other "baseline" information.</p>
<h5>Definition of Spatio-Temporal clusters</h5>
<p>In order to understand the definition of Spatio-Temporal clusters, we need to identify the differences it has against spatial cluster detection and anomaly detection. Spatial cluster detection is not the same as cluster detection: with spatial cluster detection we try to find regions where some quantity is significantly higher than expected, adjusting for the underlying population or baseline. Cluster detection just tries to find groups of data points. Neill mentions the following existing methods for clustering, but finds them lacking when faced with real life problems like predicting near repeats in burglaries.:</p>
<ul>
<li>"DBSCAN searches for points that have many other points nearby (at least m points within distance ε, where m and ε are user-specified input parameters).</li>
<li>CLIQUE aggregates points to a uniform grid and searches for grid cells containing a high proportion of points (greater than some user-specified parameter τ).</li>
<li>DENCLUE is similar to DBSCAN but uses local maxima of the density function as its starting points from which clusters are built.</li>
<li>MAFIA is an extension of CLIQUE to non-uniform grids.</li>
<li>STING is a grid-based algorithm that uses quadtree decomposition to efficiently approximate DBSCAN's results.</li>
<li>Bump hunting, which uses a greedy heuristic search (iteratively removing or adding some portion of the data such that density is maximized) to locate dense regions."</li>
</ul>
<p>Neill ends up using a modified version of the original spatial scan statistic proposed by Kulldorff. He detects spatial regions by where the underlying observations are significantly higher inside the region than outside the region: F(S)=Pr(Data|H1(s))/Pr(Data|H0(s)). He calls it the Generalized Spatial Scan Framework which works in the following manner:</p>
<ol>
<li>You first obtain data for a set of spatial locations and choose the population or expectation method to estimate the baseline:</li>
<li>Population-based method (proportion equal to its baseline). Good when we have relative rather than full information.</li>
<li>Expectation-based method (count equal to its baseline). Good when sufficient amount of historical data for a null or control condition.</li>
<li>Then you choose a set of spatial regions to search over.</li>
<li>Adjacent regions should overlap</li>
<li>Use grid lines</li>
<li>Then you choose models of data under the Null hypothesis of no clusters and the alternative hypothesis. He mentions Poisson, Gaussian, Bernoulli-Poisson (corrects false positives due to outliers), Threshold scan, Non-parametric (corrects for distributional assumptions).</li>
<li>Then Derive a score function: Fi(S)</li>
<li>Then you find the most interesting regions: F(S)*>Fi(S) for all i.</li>
<li>Finally, you conduct randomization testing (not necessary with Bayesian).</li>
</ol>
<p>Another way of detecting marginal increase is using the K-nearest neighbor analysis. Nearest neighbor analysis computes the average number of nearest neighbors for a given observation and compares the expected number of nearest neighbors to the observed mean. This type of analysis can be useful for analyzing the degree to which clustering occurs around a given observation, and whether "near-repeat" exists in the data. The k-nearest neighbor algorithm is a type of machine learning that could improve the predictive capability of near-repeat analysis.As a next step for this analysis to use k-nearest neighbors and use machine learning to explore other types of crimes and models to use, we would recommend first investigating the documentation for the Python PySal package to create a spatial weights matrix. </p>
