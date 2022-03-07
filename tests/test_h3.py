import numpy as np
import h3 as h3

#Prints out the latitude and longitude in pairs from the two numpy arrays, then gets the H3 hex from the lat lon

lat = np.load('lat.npy')
lon = np.load('lon.npy')
wind_mag = np.load('wind_mag.npy')


#H3 resolution for hexagons
resolution = 5
hexes = []

#create a list of four columns that consist of lat, lon, hex code, wind magnitude
for i, row in enumerate(lat):
	for r, nothing in enumerate(row):
		#hexes.append([lat[i][r], lon[i][r], h3.geo_to_h3(lat[i][r], lon[i][r], resolution), wind_mag[i][r]])
		hexes.append([h3.geo_to_h3(lat[i][r], lon[i][r], resolution), wind_mag[i][r]])


individual_hexes = []
#get a list of hex ids
for row in hexes:
	individual_hexes.append(row[0])

#get rid of duplicates
individual_hexes = list(set(individual_hexes))

for i in individual_hexes:
	print(i)

#####BOTTLENECK#############################
#Calculate average wind magnitude for each hex id
for i, i_hex in enumerate(individual_hexes):
	##Make each hex_id into its own list, i.e. [1,2,3,4] = [[[1]],[[2]],[[3]],[[4]]]
	individual_hexes[i] = [[individual_hexes[i]]]
	magnitude_temp = []
	for r, row in enumerate(hexes):
		if (row[0] == individual_hexes[i][0][0]):
			magnitude_temp.append(row[1])
	individual_hexes[i].append(magnitude_temp)

##This gets rid of NAN's in the one of the hexagons wind mag data
for each_hex in individual_hexes:
	i = np.array(each_hex[1])
	i = i[~np.isnan(i)]

	print(each_hex[0], np.nanmean(i))
