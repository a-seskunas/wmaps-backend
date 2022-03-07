import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
import numpy as np
##To save file without a $DISPLAY error
import matplotlib as mpl
mpl.use('Agg')
###
import pygrib
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from math import *
import g_circ as gc
import datetime
import sys
from land_sea_mask import get_land_sea_mask
import draw_lines as dc
import h3 as h3
import hex_averager as hx
from shapely.geometry import Polygon, LinearRing
from colour import Color
from mpl_toolkits.axes_grid1 import make_axes_locatable


def main(arg1, lat1, lat2, lon1, lon2, home_name, home_lat, home_lon, days, angle_start, angle_stop, wind_thresh, wave_period, thin_out, hex_size):
#def main(**kwargs):
	fig = plt.subplots(figsize=(20.5, 10.5))

	ax = plt.axes(projection=ccrs.Mercator(central_longitude=180))

	ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())

	land_feature = cfeature.NaturalEarthFeature('physical', 'land', '50m', facecolor='grey')
	ax.coastlines(resolution='50m', color='black', linewidth=2, zorder=5)
	ax.add_feature(land_feature, zorder= 5)
	ax.add_feature(cfeature.STATES.with_scale('50m'), zorder=5)
	ax.add_feature(cfeature.BORDERS, zorder=5)

	lon_vals = np.arange(lon1, lon2+10, 5)
	lat_vals = np.arange(lat1, lat2+5, 5)
	ax.set_xticks(lon_vals, crs=ccrs.PlateCarree())
	ax.set_xticklabels(lon_vals)
	ax.set_yticks(lat_vals, crs=ccrs.PlateCarree())
	ax.set_yticklabels(lat_vals)
	ax.yaxis.tick_right()
	ax.yaxis.tick_left()

	lon_formatter = cticker.LongitudeFormatter()
	lat_formatter = cticker.LatitudeFormatter()
	ax.xaxis.set_major_formatter(lon_formatter)
	ax.yaxis.set_major_formatter(lat_formatter)
	ax.grid(linewidth=1, color='grey', alpha=0.5, linestyle='--')

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
	for r, row in enumerate(lat):
		for index, l in enumerate(row):
			home_vectors[r][index] = gc.get_g_circ_angle(HOME[0], HOME[1], lat[r][index], lon[r][index])

	##Convert U and V wind components to wind direction
	wind_dir = 90. - (np.arctan2((V/magnitude), (U/magnitude)) * 180./pi + 180.)

        ###Get rid of negative wind directions. Should it happen anyway?
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

	#Thin out data points for wind arrows
	if thin_out:
		yy = np.arange(0, lon.shape[0], 1)
		xx = np.arange(0, lat.shape[1], 1)
	else:
		yy = np.arange(0, lon.shape[0], 4)
		xx = np.arange(0, lat.shape[1], 4)

	##H3 intigrations#########################
	hex_data = hx.hex_averager(hex_size, lat, lon, magnitude, magnitude)

	hexes = []
	for h in hex_data:
		cords = h3.h3_to_geo_boundary(h[0])
		##Reverse the order of coordinates, (lat, lon) -> (lon, lat)
		hex_lat, hex_lon, hex = [], [], []
		for cord in cords:
			hex_lat.append(cord[0])
			hex_lon.append(cord[1])
		for i, nothing in enumerate(hex_lat):
			hex.append((hex_lon[i], hex_lat[i]))
		hexes.append(Polygon(hex))

	##Create a color gradient map for displaying
	red = Color("red")
	blue = Color("blue")
	colors = list(blue.range_to(red, 10))
	wind_levels = np.arange(wind_thresh-5, wind_thresh+50, 5)
	wind_colors = dict(zip(wind_levels, colors))

	for i, hex in enumerate(hexes):
		if isnan(hex_data[i][1]):
			facecolor = edgecolor = Color("white")
		else:
			facecolor = wind_colors[int(round(hex_data[i][1]/5.0)*5.0)]
			edgecolor = Color("black")
		ax.add_geometries([hex], crs=ccrs.PlateCarree(), alpha=1, facecolor=facecolor.rgb, edgecolor=edgecolor.rgb)

	##make the color bar
	rgb_colors = []
	for c in colors:
		rgb_colors.append(c.rgb)
	cm = mpl.colors.ListedColormap(rgb_colors)
	####################
	norm = matplotlib.colors.Normalize()
	norm.autoscale(wind_levels)
	#cm = matplotlib.cm.copper

	sm = matplotlib.cm.ScalarMappable(cmap=cm, norm=norm)
	sm.set_array([])
	#
	points = np.meshgrid(yy, xx)
	points = tuple(points) #fix future warning from cartopy.ax.contourf(ploting wind arrows)

	pressure_levels = np.arange(950, 1032, 2)
	pressure_contour = ax.contour(lon, lat, pressure, transform=ccrs.PlateCarree(), levels=pressure_levels, zorder=6, colors='grey')
	plt.clabel(pressure_contour, inline=True, fontsize=12, fmt='%1i')
	qui = ax.quiver(lon[points], lat[points], U[points], V[points], transform=ccrs.PlateCarree(), zorder=5)
	plt.colorbar(sm)

	#for i, angle in enumerate(angles):
		#draw_swell_lines(gcs[i][0], gcs[i][1], X, C, str(angles[i]))

	P = wave_period
	num_days = np.arange(1, days)

	gc_lats = []
	gc_lons = []

	#for i, nothing in enumerate(gcs):
		#gc_lats.append(gcs[i][0][3])
		#gc_lons.append(gcs[i][1][3])


	#for i, day in enumerate(num_days):
		#get_swell_distance(P, C, str(day), gc_lats, gc_lons, home_lat, home_lon, ax)

	now = datetime.datetime.now()

	fig1 = plt.gcf()
	##Get title for chart
	grbs.seek(0)
	title = str(grbs.read(1)[0])
	print(title)
	title = title.split(':')
	plt.title(title[1][0:7] + ' wind,  '+title[6]+' '+ title[7][:-4] +',  compiled on ' + now.strftime("%b %d %H:%M") + ' UTC')
	fig1.tight_layout()
	forecast_hour = title[6][10:13].rstrip('h')
	forecast_hour = forecast_hour.strip()
	fig1.savefig('/var/www/html/images/' + home_name + 'surface_pressure'+forecast_hour+'_h3.png', dpi=80, pad_inches=0.3, bbox_inches='tight')
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
