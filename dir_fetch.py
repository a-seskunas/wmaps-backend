
import numpy as np
##To save file without a $DISPLAY error
import matplotlib as mpl
mpl.use('Agg')
###
import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from math import *
import g_circ as gc
#import data.get_data as Get_Data
import label_lines as LL
import datetime
import sys


def main(arg1, lat1, lat2, lon1, lon2, area):
	fig=plt.figure(figsize=(20.5, 10.5))
	grbs = pygrib.open('/root/sci/data/gribs/'+str(arg1))

	grb = grbs.select(name = '10 metre U wind component')[0]
	U, lat, lon = grb.data(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2)

	grb = grbs.select(name= '10 metre V wind component')[0]
	V, lat, lon = grb.data(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2)

	grb = grbs.select(name= 'Surface pressure')[0]
	pressure, lat, lon = grb.data(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2)
	pressure = pressure/100

	##Mask the pressure readings on the land
	land_sea_mask = np.load("/root/sci/land_sea_mask_temp_"+area+".dat")
	pressure = pressure * land_sea_mask
	
	###Fix this by passsing the object into the get_swell_angles and get_swell_distance functions??
	global m
	m = Basemap(projection='mill', llcrnrlat=lat1, urcrnrlat=lat2, llcrnrlon=lon1, urcrnrlon=lon2, resolution='l')

	###Whole section can be calculted once and stored, then loaded in
	###Angles can be calculated more accurately using minutes and seconds

	X = 58
	C = 'grey'

	get_swell_angles(32, 243, 49.4, 360-170, X, C, '310')
	get_swell_angles(32, 243, 43, 360-170, X, C, '300')
	get_swell_angles(32, 243, 35.75, 360-170, X, C, '290')
	get_swell_angles(32, 243, 28.5, 360-170, X, C, '280')
	get_swell_angles(32, 243, 20.65, 360-170, X, C, '270')
	get_swell_angles(32, 243, 11.9, 360-170, X, C, '260')
	###angles for the SPAC, doesn't work
	get_swell_angles(32, 243, -20, 360-170, X, C, '???')


	##Get swell distance lines and plot them
	P = 16
	
	get_swell_distance(P, C, '5')
	get_swell_distance(P, C, '4')
	get_swell_distance(P, C, '3')
	get_swell_distance(P, C, '2')
	get_swell_distance(P, C, '1')


	#magnitude = (U**2 + V**2)**0.5
	magnitude = (U**2 + V**2)**0.5 * 1.944 # convert U,V components to speed in knots
	##CALCULATE VECTOR DIRECTIONS HERE, THEN USE THEM TO FILTER BELOW

	##strip out any wind vectors that are pointing in the wrong direction
	##i.e. we only want to view vectors pointing towards the west coast
	for r, row in enumerate(U):
		for index, u in enumerate(row):
			if u < 0:
				U[r][index] = None
				V[r][index] = None
				magnitude[r][index] = None
	#########################3
	###do the same as above with the magnitude
	for r, row in enumerate(magnitude):
		for index, z in enumerate(row):
			if z < 25:
				U[r][index] = None
				V[r][index] = None
				magnitude[r][index] = None

	############################

	x, y = m(lon, lat)


	##make a matrix of indexes, used to thin out the number of data points
	yy = np.arange(0, y.shape[0], 4)
	xx = np.arange(0, x.shape[1], 4)

	points = np.meshgrid(yy, xx)

	l = np.arange(950, 1030, 2)
	m.contour(x, y, pressure, l, corner_mask=1)
	m.contourf(x, y, magnitude, [20,25,30,35,40,45,50,55,60,65,70])
	m.quiver(x[points], y[points], U[points], V[points])

	m.colorbar(pad = .7)

	m.drawparallels(np.arange(lat1, lat2, 5), labels=[1,1,0.0])
	m.drawmeridians(np.arange(lon1, lon2, 5), labels=[0,0,0,1])
	m.drawcountries()
	m.drawstates()
	m.drawcoastlines()
	m.fillcontinents()
	m.drawmapboundary()

	now = datetime.datetime.now()

	fig1 = plt.gcf()
	##Get title for chart
	grbs.seek(0)
	title = str(grbs.read(1)[0])
	title = title.split(':')
	plt.title(title[1][0:7] + ' wind,  '+title[6]+' '+ title[7][:-4] +',  compiled on ' + now.strftime("%b %d %H:%M") + ' UTC')
	##
	fig1.savefig('/var/www/html/images/' + area + 'surface_pressure'+title[6][10:11]+'.png', dpi=80)

	print "png saved at /var/www/html/images/ at " + str(datetime.datetime.now())


if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])


def get_swell_angles(lat1, lon1, lat2, lon2, X, C, label):
	lats, lons = gc.gc(lat1, lon1, lat2, lon2)
	l, o = m(lons, lats)
        m.plot(l, o, linewidth=2, color=C, label=label)
        plt.text(l[X], o[X+2]+20000, label, size=13, color=C, rotation=0)

def get_swell_distance(P, C, num_days):
	d = gc.get_period_distance(P, int(num_days))##Fix this
	dis_lats, dis_lons = gc.get_distance_points(gc.LATS, gc.LONS, d)
        l, o = m(dis_lons, dis_lats)
        m.plot(l, o, linewidth=2, color=C)
        plt.text(l[0], o[0]+40000, num_days, size=15, color=C, rotation=0)
        plt.text(l[len(l)-1], o[len(o)-1]-150000, num_days, size=15, color=C, rotation=0)
