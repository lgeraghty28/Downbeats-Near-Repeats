######################################################
#
#  Data import for City Lab efforts
#
#######################################################

from urllib import urlopen
import json
import csv


# Use app token to prevent request throttling
url = urlopen('https://data.cityofchicago.org/resource/ijzp-q8t2.json?$$app_token=riGeeqnG1oMsfm6AvIDNOoFzY').read()

data = json.loads(url)

print data[1000:1200]

