##Run DBSCAN on matrix of locations(lat and lons) of wind numbers
##Get a matrix that contains only those lat and lons of the wind


import numpy as np
###
import matplotlib as mpl
mpl.use('Agg')
###
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.impute import SimpleImputer

from time import sleep

U = np.load('U.npy')
V = np.load('V.npy')
magnitude = np.load('wind_mag.npy')
lat = np.load('lat.npy')
lon = np.load('lon.npy')

#get rid of NANs
magnitude = np.nan_to_num(magnitude)

lats = []
lons = []


for r, row in enumerate(magnitude):
	for index, i in enumerate(row):
		if magnitude[r][index] != 0:
			lats.append(lat[r][index])
			lons.append(lon[r][index])


lat_lon = np.vstack((lats, lons)).T

##Compute DBSCAN
db = DBSCAN(eps=.01, min_samples=10, algorithm="ball_tree", metric="haversine").fit_predict(np.radians(lat_lon))

print(db.shape)
labels = db


print(set(labels))
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

colors = np.random.rand(len(lats))

fig, ax = plt.subplots(figsize=[10, 6])
df_scatter = ax.scatter(lons, lats, c=colors, alpha=0.9, s=3)
ax.set_title('Full data set vs DBSCAN reduced set')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
fig.savefig('/var/www/html/images/classifier.png', dpi=80, pad_inches=0.3, bbox_inches='tight')
