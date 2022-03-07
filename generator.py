import sys
import dir_fetch
from os import listdir
import h3_dir_fetch

grib_files = []

grib_files = listdir('/home/adam/sci/data/gribs')


##h3 tester
#for f in grib_files:
        #h3_dir_fetch.main(f, 30, 45, 225, 245, 'SD_wind', 32.7, 242.85, 5, 160, 310, 10, 10, True, 4)
for f in grib_files:
	dir_fetch.main(f, 10, 60, 150, 245, 'SD_N', 32, 243, 9, 160, 310, 25, 16, False)
	#h3_dir_fetch.main(f, 10, 60, 150, 245, 'SD_N', 32, 243, 9, 160, 310, 25, 16, False, 3)
#for f in grib_files:
	#h3_dir_fetch.main(f, 10, 45, 280, 340, 'LBI', 40.5, 360-73.7, 10, 80, 210, 15, 12, False, 3)
##same as above, but for the South Pacific
#for f in grib_files:
	#dir_fetch.main(f, -70, -10, 130, 290, 'SD_S', 32, 243, 13, 160, 310, 25, 18)
	#h3_dir_fetch.main(f, -70, -10, 130, 290, 'SD_S', 32, 243, 13, 160, 310, 25, 18, False, 1)

