
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


def main(arg1):
	fig=plt.figure(figsize=(20.5, 10.5))
	grbs = pygrib.open('/root/sci/data/gribs/'+str(arg1))

	grb = grbs.select(name = '10 metre U wind component')[0]
	U, lat, lon = grb.data(lat1=10, lat2=60, lon1=150, lon2=245)

	grb = grbs.select(name= '10 metre V wind component')[0]
	V, lat, lon = grb.data(lat1=10, lat2=60, lon1=150, lon2=245)

	grb = grbs.select(name= 'Surface pressure')[0]
	pressure, lat, lon = grb.data(lat1=10, lat2=60, lon1=150, lon2=245)
	pressure = pressure/100

	##Mask the pressure readings on the land
	land_sea_mask = np.load("land_sea_mask.dat")
	pressure = pressure * land_sea_mask


	m = Basemap(projection='mill', llcrnrlat=10, urcrnrlat=60, llcrnrlon=150, urcrnrlon=245, resolution='l')

	###Whole section can be calculted once and stored, then loaded in
	###Angles can be calculated more accurately using minutes and seconds

	X = 58
	C = 'grey'


	lats, lons = gc.gc(32, 243, 49.4, 360-170)##310 degrees, add label
	l, o = m(lons, lats)
	m.plot(l, o, linewidth=2, color=C, label="310")
	plt.text(l[X], o[X+2]+20000, '310', size=13, color=C, rotation=0)

	lats, lons = gc.gc(32, 243, 43, 360-170)##300 degrees add label
	l, o = m(lons, lats)
	m.plot(l, o, linewidth=2, color=C)
	plt.text(l[X], o[X+1]+40000, '300', size=13, color=C, rotation=0)

	lats, lons = gc.gc(32, 243, 35.75, 360-170)##290 degrees add label
	l, o = m(lons, lats)
	m.plot(l, o, linewidth=2, color=C)
	plt.text(l[X-1], o[X-5], '290', size=13, color=C, rotation=0)

	lats, lons = gc.gc(32, 243, 28.5, 360-170)##280 degrees add label
	l, o = m(lons, lats)
	m.plot(l, o, linewidth=2, color=C)
	plt.text(l[X-2], o[X+3], '280', size=13, color=C, rotation=0)

	lats, lons = gc.gc(32, 243, 20.65, 360-170)##270 degrees add label
	l, o = m(lons, lats)
	m.plot(l, o, linewidth=2, color=C)
	plt.text(l[X-3], o[X+2], '270', size=13, color=C, rotation=0)

	lats, lons = gc.gc(32, 243, 11.9, 360-170)##260 degrees add label
	l, o = m(lons, lats)
	m.plot(l, o, linewidth=2, color=C)
	plt.text(l[X-4], o[X], '260', size=13, color=C, rotation=0)

	##Get swell distance lines and plot them
	P = 16

	d = gc.get_period_distance(P, 5)

	dis_lats, dis_lons = gc.get_distance_points(gc.LATS, gc.LONS, d)
	l, o = m(dis_lons, dis_lats)
	m.plot(l, o, linewidth=2, color=C)
	plt.text(l[0], o[0]+40000, '5', size=15, color=C, rotation=0)
	plt.text(l[len(l)-1], o[len(o)-1]-150000, '5', size=15, color=C, rotation=0)


	d = gc.get_period_distance(P, 4)
	dis_lats, dis_lons = gc.get_distance_points(gc.LATS, gc.LONS, d)
	l, o = m(dis_lons, dis_lats)
	m.plot(l, o, linewidth=2, color=C)
	plt.text(l[0], o[0]+40000, '4', size=15, color=C, rotation=.2)
	plt.text(l[len(l)-1], o[len(o)-1]-150000, '4', size=15, color=C, rotation=.2)

	d = gc.get_period_distance(P, 3)
	dis_lats, dis_lons = gc.get_distance_points(gc.LATS, gc.LONS, d)
	l, o = m(dis_lons, dis_lats)
	m.plot(l, o, linewidth=2, color=C)
	plt.text(l[0], o[0]+40000, '3', size=15, color=C, rotation=.2)
	plt.text(l[len(l)-1], o[len(o)-1]-150000, '3', size=15, color=C, rotation=.2)

	d = gc.get_period_distance(P, 2)
	dis_lats, dis_lons = gc.get_distance_points(gc.LATS, gc.LONS, d)
	l, o = m(dis_lons, dis_lats)
	m.plot(l, o, linewidth=2, color=C)
	plt.text(l[0], o[0]+40000, '2', size=15, color=C, rotation=.2)
	plt.text(l[len(l)-1], o[len(o)-1]-150000, '2', size=15, color=C, rotation=.2)

	d = gc.get_period_distance(P, 1)
	dis_lats, dis_lons = gc.get_distance_points(gc.LATS, gc.LONS, d)
	l, o = m(dis_lons, dis_lats)
	m.plot(l, o, linewidth=2, color=C)
	plt.text(l[0], o[0]+40000, '1', size=15, color=C, rotation=.2)
	plt.text(l[len(l)-1], o[len(o)-1]-150000, '1', size=15, color=C, rotation=.2)

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
	m.contour(x, y, pressure, l)
	m.contourf(x, y, magnitude, [20,25,30,35,40,45,50,55,60,65,70])
	m.quiver(x[points], y[points], U[points], V[points])

	m.colorbar(pad = .7)

	m.drawparallels(np.arange(10, 60, 5), labels=[1,1,0.0])
	m.drawmeridians(np.arange(150, 245, 5), labels=[0,0,0,1])
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
	fig1.savefig('/var/www/html/images/surface_pressure'+title[6][10:11]+'.png', dpi=80)

	print "png saved at /var/www/html/images/ at " + str(datetime.datetime.now())


if __name__ == "__main__":
	main(sys.argv[1])
