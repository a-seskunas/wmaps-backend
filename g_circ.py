import math as m
import numpy as np

def travel_time(lat2, lon2, lat1=32, lon1=243, period=16):
	distance = gc_distance(lat1, lon1, lat2, lon2)
	speed = period * 1.56
	time = distance/speed
	return time

def ll_to_xyz(lat, lon):
	x = m.cos(m.radians(lat))*m.cos(m.radians(lon))
	y = m.cos(m.radians(lat))*m.sin(m.radians(lon))
	z = m.sin(m.radians(lat))
	return x, y, z

def gc(lat1, lon1, lat2, lon2, num_points=500):
	p1 = ll_to_xyz(lat1, lon1)
	p2 = ll_to_xyz(lat2, lon2)
	w = np.cross(np.cross(p1,p2), p1)
	mag = np.linalg.norm(w)
	w = [w[0]/mag, w[1]/mag, w[2]/mag]
	angles = np.linspace(0, 2*np.pi, num_points)
	gc = []
	for a in angles:
		x = np.multiply(p1, m.cos(a))
		y = np.multiply(w, m.sin(a))
		gc.append([x[0]+y[0], x[1]+y[1], x[2]+y[2]])
	points = []
	for c in gc:
		points.append(xyz_to_lat(c[0],c[1],c[2]))
	lats = []
	lons = []
	for p in points:
		if p[0] > 0 and p[0] < 99:
			lats.append(p[0])
			if p[1] < 0:
				lons.append(p[1]+360)
			else:
				lons.append(p[1])
	return lats, lons

def xyz_to_lat(x,y,z):
	lat = m.atan2(z, m.hypot(x,y))
	lon = m.atan2(y, x)
	return m.degrees(lat), m.degrees(lon)

def gc_distance(lat1, lon1, lat2, lon2):
	a = ll_to_xyz(lat1, lon1)
	b = ll_to_xyz(lat2, lon2)
	##Radius of the earf
	R = 3959
	distance = R * m.atan2(np.linalg.norm(np.cross(a, b)), np.dot(a,b))
	return distance


def roundup(x):
##Rounds a number up to the neartest 10
	return int(m.ceil(x/10.0))*10

def get_period_distance(period=16, days=3):
	distance = (period*1.56)*(days*24)
	return distance

def get_distance_values(lats, lons, distance):
##Takes a great circle line consisting of latitudes and longitudes, returns the latitude and longitude
##of that distance
	for c, value in enumerate(lats):
		#print roundup(gc_distance(32, 243, lats[c], lons[c])), roundup((period*1.56)*(3*24))
		if roundup(gc_distance(32, 243, lats[c], lons[c])) == roundup(distance):
			return lats[c], lons[c]

####Points on great circle lines, used to get distances
LATS = [49.4, 46, 43, 39.3, 35.75, 32.1, 28.5, 24.7, 20.65, 16.5, 11.9]
LONS = [190, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190]
##########


def get_distance_points(LATS, LONS, distance):
##Returns a list of latitudes and longitudes of equal distance along several(LATS, LONS) great circles
	dis_lats = []
	dis_lons = []

	for c, value in enumerate(LATS):
		lats, lons = gc(32, 243, LATS[c], LONS[c])
		d_lats, d_lons = get_distance_values(lats, lons, distance)
		dis_lats.append(d_lats)
		dis_lons.append(d_lons)

	return dis_lats, dis_lons


def get_g_circ_angle(latA, lonA, latB, lonB):
##Returns the angle along the great circle path from A to B
	a = ll_to_xyz(latA, lonA)
	b = ll_to_xyz(latB, lonB)
	N = (0,0,1)##North pole in vector form
	c1 = np.cross(a, b)
	c2 = np.cross(a, N)

	sin_theta = np.linalg.norm(np.cross(c1, c2)) * np.sign(np.dot(np.cross(c1,c2), a))
	t = m.atan2(sin_theta, np.dot(c1, c2))

	theta = (m.degrees(t) +360) % 360
	return theta

t = get_g_circ_angle(32, 360-117, 16.5, 360-170)
print t
