#!/usr/bin/python

import get_data as Get_Data
import datetime
import time


date = datetime.date.today()
datestring = (date.strftime('%Y%m%d'))

print(datestring)

for num_runs in range(1):
	times = ["000", "012", "024", "048", "072"]
	Get_Data.get_sample_data_https(datestring, "00", times[num_runs])
	print("Got " + times[num_runs] +"Z grib at " + str(datetime.datetime.now()))
	#time.sleep(60)
