
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


def get_swell_angles(lat1, lon1, lat2, lon2, X, C, label):
        #uses the great circle(gc) function to plot the swell angle lines
        lats, lons = gc.gc(lat1, lon1, lat2, lon2, 300)
	lons, lats = m.shiftdata(lons, lats)
        l, o = m(lons, lats)
        m.plot(l, o, linewidth=2, color=C, marker='.', label=label)
        #plt.text(l[X], o[X+2]+20000, label, size=13, color=C, rotation=0)

def get_swell_distance(P, C, num_days):
        #uses the great circle(gc) function to plot the swell distance lines
        d = gc.get_period_distance(P, int(num_days))##Fix this
        dis_lats, dis_lons = gc.get_distance_points(gc.LATS, gc.LONS, d)
        l, o = m(dis_lons, dis_lats)
        m.plot(l, o, linewidth=2, color=C)
        #plt.text(l[0], o[0]+40000, num_days, size=15, color=C, rotation=0)
        #plt.text(l[len(l)-1], o[len(o)-1]-150000, num_days, size=15, color=C, rotation=0)

lat1 = -50
lat2 = 50
lon1 = 100
lon2 = 290


m = Basemap(projection='mill', llcrnrlat=lat1, urcrnrlat=lat2, llcrnrlon=lon1, urcrnrlon=lon2, resolution='l')

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

#get_swell_distance(P, C, '5')
#get_swell_distance(P, C, '4')
#get_swell_distance(P, C, '3')
#get_swell_distance(P, C, '2')
#get_swell_distance(P, C, '1')

m.drawparallels(np.arange(lat1, lat2, 5), labels=[1,1,0.0])
m.drawmeridians(np.arange(lon1, lon2, 5), labels=[0,0,0,0])
m.drawcountries()
m.drawstates()
m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()


fig1 = plt.gcf()
fig1.savefig('/var/www/html/images/great_circle_test.png', dpi=80)

print "png saved at /var/www/html/images/ at " + str(datetime.datetime.now())



