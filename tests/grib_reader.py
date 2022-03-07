##opens grib file and prints out headers

import pygrib

#grbs = pygrib.open('/root/sci/data/sample_gribs/stuff000.grb2')
#grbs = pygrib.open('/root/sci/data/sample_gribs/sample.grb2')
grbs = pygrib.open('/root/sci/data/gribs/stuff036.grb2')

#grb  = grbs.read(1)[0]
#grb.keys()
#grbs.seek(0)

#for grb in grbs:
        #print grb

#grbs.rewind()

#for grb in grbs:
	#print grb.name

grbs.seek(0)
title = str(grbs.read(1)[0])
print(title)
title = title.split(':')
print title[6][10:13]
