# Grabbing json file with Socrata
# Download the RSocrata file from https://github.com/Chicago/RSocrata/releases/tag/v1.5.1
# Install via install.packages("/path/to/RSocrata-1.5.1.tar.gz", repo=NULL, type='source')
# via interactive R.

library('RSocrata')
crimes.data <- ('https://data.cityofchicago.org/resource/ijzp-q8t2.json')

