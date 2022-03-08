import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
import numpy as np
##To save file without a $DISPLAY error
import matplotlib as mpl
mpl.use('Agg')
###
import pygrib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from math import *
import g_circ as gc
import datetime
import sys
from land_sea_mask import get_land_sea_mask
import draw_lines as dc
import image_to_db as to_db
import sqlite3
import pickle

import time

def main(arg1, lat1, lat2, lon1, lon2, home_name, home_lat, home_lon, days, angle_start, angle_stop, wind_thresh, wave_period, thin_out):

	infile = open(home_name + "_base.pkl", 'rb')
	ax = pickle.load(infile)
	infile.close()

	grbs = pygrib.open('/home/adam/sci/data/gribs/'+str(arg1))

	grb = grbs.select(name = '10 metre U wind component')[0]
	U, lat, lon = grb.data(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2+5)

	grb = grbs.select(name= '10 metre V wind component')[0]
	V, lat, lon = grb.data(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2+5)

	#grb = grbs.select(name= 'MSLP (Eta model reduction)')[0]
	grb = grbs.message(1)
	pressure, lat, lon = grb.data(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2+5)
	pressure = pressure/100


	X = 30
	C = 'grey'
	circle_length = radians(lon2-lon1)

	gcs, angles = dc.draw_lines([home_lat, home_lon], angle_start, angle_stop, circle_length)

	magnitude = (U**2 + V**2)**0.5 * 1.944 # convert U,V components to speed in knots
	##CALCULATE VECTOR DIRECTIONS HERE, THEN USE THEM TO FILTER BELOW
	HOME = [home_lat, home_lon]
	home_vectors = np.zeros(np.shape(lat))

	##Convert U and V wind components to wind direction
	wind_dir = 90. - (np.arctan2((V/magnitude), (U/magnitude)) * 180./pi + 180.)
        ###Get rid of negative wind directions, better way to do this?  Should it happen anyway?
	wind_dir[wind_dir < 0] = 360 + wind_dir[wind_dir < 0]

	##strip out any wind vectors that are pointing in the wrong direction
	##i.e. we only want to view vectors pointing towards the west coast
	msk = abs(home_vectors - wind_dir) > 50
	U[msk] = None
	V[msk] = None
	magnitude[msk] = None

	###do the same as above with the magnitude
	wind_msk = (magnitude < wind_thresh)
	U[wind_msk] = None
	V[wind_msk] = None
	magnitude[wind_msk] = None

	############################
	#Thin out data points for wind arrows
	if thin_out:
		yy = np.arange(0, lon.shape[0], 1)
		xx = np.arange(0, lat.shape[1], 1)

	else:
		yy = np.arange(0, lon.shape[0], 4)
		xx = np.arange(0, lat.shape[1], 4)

	points = np.meshgrid(yy, xx)
	points = tuple(points) #fix future warning from cartopy.ax.contourf(ploting wind arrows)


	wind_levels = np.arange(wind_thresh-5, wind_thresh+50, 5)

	pressure_levels = np.arange(950, 1032, 2)
	pressure_contour = ax.contour(lon, lat, pressure, transform=ccrs.PlateCarree(), levels=pressure_levels, zorder=6, colors='grey')
	plt.clabel(pressure_contour, inline=True, fontsize=12, fmt='%1i')
	wind_contour = ax.contourf(lon, lat, magnitude, transform=ccrs.PlateCarree(), levels=wind_levels, zorder=4)
	ax.quiver(lon[points], lat[points], U[points], V[points], transform=ccrs.PlateCarree(), zorder=5)
	color_bar = plt.colorbar(wind_contour, shrink=.9, pad=.05)

	P = wave_period
	num_days = np.arange(1, days)

	gc_lats = []
	gc_lons = []

	for i, nothing in enumerate(gcs):
		gc_lats.append(gcs[i][0][3])
		gc_lons.append(gcs[i][1][3])

	now = datetime.datetime.now()

	fig1 = plt.gcf()
	##Get title for chart
	grbs.seek(0)
	title = str(grbs.read(1)[0])
	print(title)
	title = title.split(':')
	plt.title(title[1][0:7] + ' wind,  '+title[6]+' '+ title[7][:-4] +',  compiled on ' + now.strftime("%b %d %H:%M") + ' UTC')
	#fig1.tight_layout()
	forecast_hour = title[6][10:13].rstrip('h')
	forecast_hour = forecast_hour.strip()
	fig1.savefig('/var/www/html/images/' + home_name + 'surface_pressure'+forecast_hour+'.png', dpi=80, pad_inches=0.3, bbox_inches='tight')
	##save the 00Z image in the past images folder for long term storage
	if forecast_hour == '0':
		path_to_past_image = '/var/www/html/images/past_images/' + home_name + now.strftime("%Y-%m-%d_%H") + '.png'
		fig1.savefig(path_to_past_image, dpi=60, pad_inches=0.3, bbox_inches='tight')
		print('past image saved at ' + path_to_past_image)

		##add the path to the image to the database
		conn = sqlite3.connect("/home/adam/sci/db/image_paths.db")
		with conn:
			im_name = home_name + now.strftime("%Y-%m-%d_%H") + '.png'
			image = (path_to_past_image, now.strftime("%Y-%m-%d"), now.strftime("%H"), home_name, im_name)
			image_id = to_db.create_image(conn, image)
			print(image_id)
	plt.close("all")
	print('png saved at /var/www/html/images/ at ' + '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

if __name__ == "__main__":
	main(*sys.argv)

def draw_swell_lines(lats, lons, X, C, label):
	plt.plot(lons, lats, transform=ccrs.PlateCarree(), zorder=2, color='grey', linewidth=1)
        #plt.text(l[X], o[X+2]+20000, label, size=13, color=C, rotation=0)

def get_swell_distance(P, C, num_days, lats, lons, home_lat, home_lon, ax):
	#uses the great circle(gc) function to plot the swell distance lines
	d = gc.get_period_distance(P, int(num_days))
	dis_lats, dis_lons = gc.get_distance_points(lats, lons, d, home_lat, home_lon)
	plt.plot(dis_lons, dis_lats, transform=ccrs.PlateCarree(), zorder=2, color='grey', linewidth=1)
	#plt.figtext(l[0]-10000, o[0]-10000, num_days, size=15, color=C, rotation=0, zorder=1)
	#plt.text(l[0], o[0], num_days, size=15, color=C, rotation=0)
	#plt.figtext(l[len(l)-1], o[len(o)-1], num_days, size=15, color=C, rotation=0, zorder=1)

	#plt.text(0, 0, "THis is only a test")
	#print l[0], o[0], l[local_min], l[local_max], o[local_min], o[local_max]