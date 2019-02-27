import urllib2
import urllib


def get_data_https(DATE, HOUR="00", FORECAST_HOUR="000"):
	 ##NOMADS grib filter, returns just UGRD and VGRD wind components .25 grid spacing, 10m above sea level
	url = "http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t"+HOUR+"z.pgrb2.0p25.f"+FORECAST_HOUR+"&lev_surface=on&lev_10_m_above_ground=on&var_PRES=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs."+DATE+HOUR
	response = urllib2.urlopen(url)
	fh = open("/root/sci/data/gribs/stuff"+FORECAST_HOUR+".grb2", "wb")
	fh.write(response.read())
	fh.close()


def get_data(DATE, HOUR="00", FORECAST_HOUR="000"):
	###NOMADS grib filter, returns just UGRD and VGRD wind components .25 grid spacing, 10m above sea level
	url = "http://nomads.ncep.noaa.gov/cgi-bin/filter_gdas_0p25.pl?file=gdas.t00z.pgrb2.0p25.f000&lev_surface=on&all_var=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgdas.20181207"
	urllib.urlretrieve(url, "/root/sci/data/gribs/stuff"+FORECAST_HOUR+".grb2")
	return None



