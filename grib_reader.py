##opens grib file and prints out headers

import pygrib

grbs = pygrib.open('/root/sci/data/gribs/sample.grb2')

grb  = grbs.read(1)[0]
#grb.keys()
grbs.seek(0)

for grb in grbs:
        print grb
