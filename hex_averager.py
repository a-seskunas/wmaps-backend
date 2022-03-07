import numpy as np
import h3 as h3


def hex_averager(resolution, lat, lon, wind_mag, wind_dir):
	hexes = []

	#create a list of 3 columns that consist of hex code, wind magnitude, wind direction
	for i, row in enumerate(lat):
		for r, nothing in enumerate(row):
			hexes.append([h3.geo_to_h3(lat[i][r], lon[i][r], resolution), wind_mag[i][r], wind_dir[i][r]])

	individual_hexes = []

	##REPLACE THIS WITH A STRIAGHT ASSIGMENT OF THE FIRST COLOMN OF HEXES
	#get a list of hex ids
	for row in hexes:
		individual_hexes.append(row[0])

	#get rid of duplicates
	individual_hexes = list(set(individual_hexes))

	hexes = np.array(hexes)

	hex_averages = []

	#Calculate average wind magnitude for each hex id
	##Add the average for the wind direction with something like np.nanmean(vals[:,2].astype(float)
	for i, i_hex in enumerate(individual_hexes):
		vals = hexes[hexes[:,0] == i_hex]
		hex_averages.append([i_hex, np.nanmean(vals[:,1].astype(float))])


	return hex_averages
