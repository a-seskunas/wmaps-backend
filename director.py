import sys
import dir_fetch
from os import listdir

grib_files = []

grib_files = listdir('/root/sci/data/gribs')

##generate an image from the grib file
#for f in grib_files:
	#dir_fetch.main(f)

dir_fetch.main('sample.grb2')
