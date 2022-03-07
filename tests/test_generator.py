####Generates a base map for each zone, defined by the home_name variable
####Calls the generator, which uses the variables given to make the basemap

import sys
import generator as generator
from os import listdir

grib_files = []
grib_files = listdir('/home/adam/sci/data/gribs')
grib_file = grib_files[0]

##dir_fetch(arg1, lat1, lat2, lon1, lon2, home_name, home_lat, home_lon, days, angle_start, angle_stop, wind_thresh, wave_period, thin_out)

##generate the basemap for each zone
generator.main(grib_file, 10, 60, 150, 245, 'SD_N', 32.7, 242.85, 9, 160, 310, 25, 16, False)
generator.main(grib_file, 30, 45, 225, 245, 'SD_wind', 32.7, 242.85, 5, 160, 310, 10, 10, True)
generator.main(grib_file, 10, 45, 280, 340, 'LBI', 40.5, 360-73.7, 10, 80, 210, 15, 12, False)
generator.main(grib_file, -70, -10, 130, 290, 'SD_S', 32.7, 242.85, 13, 160, 310, 25, 18, False)

