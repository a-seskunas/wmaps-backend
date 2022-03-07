
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
import label_lines as LL
import datetime
import sys
from land_sea_mask import get_land_sea_mask


def draw_lines(home, angle_start, angle_stop, circle_length):
	angles = np.arange(angle_start, angle_stop+10, 10)
	great_circles = []

	for angle in angles:
		d_p = gc.destination_point(home[0], home[1], angle)
		great_circles.append(gc.gc(home[0], home[1], d_p[0], d_p[1], circle_length))

	great_circles = np.array(great_circles)

	return great_circles, angles



