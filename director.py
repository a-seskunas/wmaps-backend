import sys
import dir_fetch
from os import listdir

grib_files = []

grib_files = listdir('/root/sci/data/gribs')

##generate an image from the grib file for the North Pacific
for f in grib_files:
	dir_fetch.main(f, 10, 60, 150, 245, 'N')

##same as above, but for the South Pacific
for f in grib_files:
	dir_fetch.main(f, -70, -10, 130, 290, 'S')
