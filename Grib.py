# Grib.py
# A class to help manipulate grib files
# Initialize with a grib object opened with pygrib

from numpy import meshgrid as meshgrid
from numpy import arange as arange

class Grib:
    def __init__(self, grib, coordinates):
        self.grib = grib
        self.lat1, self.lat2, self.lon1, self.lon2 = coordinates

        grb = grib.select(name="10 metre U wind component")[0]
        self.U, self.lats, self.lons = grb.data(*coordinates)

        grb = grib.select(name="10 metre V wind component")[0]
        self.V = grb.data(*coordinates)[0]

        grb = grib.message(1)
        pressure = grb.data(*coordinates)[0]
        self.pressure = pressure / 100

        self.magnitude = (
                self.U**2 + self.V**2
        ) ** 0.5 * 1.944
   
    def thin_out(self, screen_size=1):
        '''Return an array of the correct shape that can be used to thin out
        a field.  i.e. U[thined_out]'''

        yy = arange(0, self.lons.shape[0], screen_size)
        xx = arange(0, self.lats.shape[1], screen_size)

        points = tuple(meshgrid(yy, xx))
        return points
