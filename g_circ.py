import math as m
import numpy as np


def draw_lines(home, angle_start, angle_stop, circle_length):
	angles = np.arange(angle_start, angle_stop+10, 10)
	great_circles = []

	for angle in angles:
		d_p = destination_point(home[0], home[1], angle)
		great_circles.append(gc(home[0], home[1], d_p[0], d_p[1], circle_length))

	great_circles = np.array(great_circles)

	return great_circles, angles
    
def destination_point(lat, lon, start_angle, angular_distance=m.pi/4):
	angle = m.radians(start_angle)
	N = (0,0,1)
	a = ll_to_xyz(lat, lon)
	d_e = np.cross(N, a)
	d_n = np.cross(a, d_e)
	d = np.multiply(d_n, np.cos(angle)) + np.multiply(d_e, np.sin(angle))
	b = np.multiply(a, np.cos(angular_distance)) + np.multiply(d,  np.sin(angular_distance))
	destination_point = xyz_to_lat(b[0], b[1], b[2])
	return destination_point

def travel_time(lat2, lon2, lat1=32, lon1=243, period=16):
	distance = gc_distance(lat1, lon1, lat2, lon2)
	speed = period * 1.56
	time = distance/speed
	return time

def ll_to_xyz(lat, lon):
	x = np.cos(np.radians(lat))*np.cos(np.radians(lon))
	y = np.cos(np.radians(lat))*np.sin(np.radians(lon))
	z = np.sin(np.radians(lat))
	return x, y, z

def gc(lat1, lon1, lat2, lon2, circle_length, num_points=1000):
	p1 = ll_to_xyz(lat1, lon1)
	p2 = ll_to_xyz(lat2, lon2)
	w = np.cross(np.cross(p1,p2), p1)
	mag = np.linalg.norm(w)
	w = [w[0]/mag, w[1]/mag, w[2]/mag]
	angles = np.linspace(0, circle_length, num_points)
	gc = []
	for a in angles:
		x = np.multiply(p1, np.cos(a))
		y = np.multiply(w, np.sin(a))
		gc.append([x[0]+y[0], x[1]+y[1], x[2]+y[2]])
	points = []
	for c in gc:
		points.append(xyz_to_lat(c[0],c[1],c[2]))
	lats = []
	lons = []
	for p in points:
		if p[0] > -99 and p[0] < 99:
			lats.append(p[0])
			if p[1] < 0:
				lons.append(p[1]+360)
			else:
				lons.append(p[1])
	return lats, lons

def xyz_to_lat(x,y,z):
	lat = np.arctan2(z, np.hypot(x,y))
	lon = np.arctan2(y, x)
	return np.degrees(lat), np.degrees(lon)

def gc_distance(lat1, lon1, lat2, lon2):
	a = ll_to_xyz(lat1, lon1)
	b = ll_to_xyz(lat2, lon2)
	##Radius of the earf
	R = 3959
	distance = R * np.arctan2(np.linalg.norm(np.cross(a, b)), np.dot(a,b))
	return distance


def roundup10(x):
##Rounds a number up to the neartest 10
	return int(m.ceil(x/10.0))*10

def roundup200(x):
	return int(m.ceil(x/200.))*200

def get_period_distance(period=16, days=3):
	distance = (period*1.56)*(days*24)
	return distance

def get_distance_values(lats, lons, distance, home_lat, home_lon):
##Takes a great circle line consisting of latitudes and longitudes, returns the latitude and longitude
##of the distance given, along the circle
	for c, value in enumerate(lats):
		if roundup10(gc_distance(home_lat, home_lon, lats[c], lons[c])) == roundup10(distance):
			return lats[c], lons[c]


def get_distance_points(gc_lats, gc_lons, distance, home_lat, home_lon):
##Returns a list of latitudes and longitudes of equal distance along several great circles
#gc_lats and gc_lons should be lists of points on several great circles
	dis_lats = []
	dis_lons = []

	for c, value in enumerate(gc_lats):
		lats, lons = gc(home_lat, home_lon, gc_lats[c], gc_lons[c], 2.5)
		d_lats, d_lons = get_distance_values(lats, lons, distance, home_lat, home_lon)
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

	theta = (np.degrees(t) +360) % 360
	return theta

#Bearing from A to B along the great circle path
#Output is 0 for North, 90 is east, 180 is south, 270(or -90) is west
def get_g_circ_bearing(latA, lonA, latB, lonB):
	latA, lonA, latB, lonB = np.radians(latA), np.radians(lonA), np.radians(latB), np.radians(lonB)
	S = np.cos(latB) * np.sin((lonA - lonB))
	C = np.cos(latA) * np.sin(latB) - np.sin(latA)*np.cos(latB)*np.cos((lonA-lonB))
	beta = np.arctan2(S,C)
	#return np.degrees(beta)
	return (np.degrees(beta) + 360) % 360
