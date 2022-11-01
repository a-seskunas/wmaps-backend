from Grib import Grib
import pytest
import pygrib

@pytest.fixture
def sample_grib(): 
    sample_grib = pygrib.open("/home/adam/sci/data/sample_gribs/sample.grb2")
    return sample_grib

@pytest.fixture
def area():
    area = [10, 60, 150, 245]
    return area 

@pytest.fixture
def grib_area(sample_grib, area):
    grib_area = Grib(sample_grib, area)
    sample_grib.close()
    return grib_area

def test_init(grib_area):
    assert grib_area is not None
    assert grib_area.lat1 == 10
    assert grib_area.lat2 == 60
    assert grib_area.lon1 == 150
    assert grib_area.lon2 == 245
    assert grib_area.V.shape == grib_area.U.shape
    assert grib_area.V.shape == grib_area.magnitude.shape
    assert grib_area.U.shape == grib_area.magnitude.shape
    assert grib_area.U.shape == ((grib_area.lat2 - grib_area.lat1)*4 + 1, (grib_area.lon2 - grib_area.lon1)*4 + 1)
