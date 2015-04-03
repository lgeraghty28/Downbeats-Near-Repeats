######################################################
#
#  Data import for City Lab efforts
#
#######################################################

from urllib import urlopen
import json


url = urlopen('https://data.cityofchicago.org/resource/ijzp-q8t2.json').read()
data = json.loads(url)
print data[0:10]


