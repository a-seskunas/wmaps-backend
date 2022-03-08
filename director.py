import sys
import h3_dir_fetch
import dir_fetch
from os import listdir
import time

grib_files = []

grib_files = listdir('/home/adam/sci/data/gribs')

#Wrap in try, except to catch Value errors


##dir_fetch(arg1, lat1, lat2, lon1, lon2, home_name, home_lat, home_lon, days, angle_start, angle_stop, wind_thresh, wave_period, thin_out)

start_time = time.time()

##generate an image from the grib file for the North Pacific
for f in grib_files:
	dir_fetch.main(f, 10, 60, 150, 245, 'SD_N', 32.7, 242.85, 9, 160, 310, 25, 16, False)
	dir_fetch.main(f, 30, 45, 225, 245, 'SD_wind', 32.7, 242.85, 5, 160, 310, 10, 10, True)
	dir_fetch.main(f, 10, 45, 280, 340, 'LBI', 40.5, 360-73.7, 10, 80, 210, 15, 12, False)
	dir_fetch.main(f, -70, -10, 130, 290, 'SD_S', 32.7, 242.85, 13, 160, 310, 25, 18, False)

end_time = time.time()
print(f"Execution time: {round(end_time-start_time, 2)}")

