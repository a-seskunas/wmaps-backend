###Gets the land-sea mask from the sample.grib, then saves it
###so it can be used by any program

import pygrib
import numpy as np

grbs = pygrib.open('/root/sci/data/sample_gribs/sample.grb2')

grb = grbs.select(name= 'Land-sea mask')[0]
land_sea_mask, lat, lon = grb.data(lat1=10, lat2=60, lon1=150, lon2=245)

###The sea is masked, we want the land masked, so "invert" the matrix
land_sea_mask = np.logical_not(land_sea_mask).astype(int)

land_sea_mask.dump("land_sea_mask_temp.dat")
