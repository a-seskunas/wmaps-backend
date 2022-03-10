from urllib.request import urlopen


def get_data_https(DATE, HOUR="00", FORECAST_HOUR="000"):
    ##NOMADS grib filter, returns just UGRD and VGRD wind components .25 grid spacing, 10m above sea level
    url = (
        "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t"
        + HOUR
        + "z.pgrb2.0p25.f"
        + FORECAST_HOUR
        + "&lev_mean_sea_level=on&lev_10_m_above_ground=on&var_MSLET=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs."
        + DATE
        + "%2F"
        + HOUR
        + "%2Fatmos"
    )

    response = urlopen(url)
    fh = open("/home/adam/sci/data/gribs/stuff" + FORECAST_HOUR + ".grb2", "wb")
    fh.write(response.read())
    fh.close()


def get_sample_data_https(DATE, HOUR="00", FORECAST_HOUR="000"):
    url = (
        "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t00z.pgrb2.0p25.anl"
        "&lev_20_m_above_ground=on&lev_mean_sea_level=on&var_MSLET=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs."
        + DATE
        + "%2F00%2Fatmos"
    )
    print(url)
    response = urlopen(url)
    fh = open("/home/adam/sci/data/sample_gribs/stuff" + FORECAST_HOUR + ".grb2", "wb")
    fh.write(response.read())
    fh.close()
