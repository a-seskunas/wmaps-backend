###Gets the land-sea mask from the sample.grib, then saves it
###so it can be used by any program

#import pygrib
#import numpy as np
def get_land_sea_mask(lat1, lat2, lon1, lon2):
	grbs = pygrib.open('/root/sci/data/sample_gribs/sample.grb2')

	grb = grbs.select(name= 'Land-sea mask')[0]
	#land_sea_mask, lat, lon = grb.data(lat1=10, lat2=60, lon1=150, lon2=245)
	#land_sea_mask, lat, lon = grb.data(lat1=-70, lat2=-10, lon1=130, lon2=290)
	#land_sea_mask, lat, lon = grb.data(lat1=10, lat2=45, lon1=280, lon2=340)
	land_sea_mask, lat, lon = grb.data(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2)

	###The sea is masked, we want the land masked, so "invert" the matrix
	land_sea_mask = np.logical_not(land_sea_mask).astype(int)

	land_sea_mask.dump("land_sea_mask_temp_B_I.dat")
