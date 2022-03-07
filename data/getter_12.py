#!/usr/bin/python

import get_data as Get_Data
import datetime
import time

date = datetime.date.today()
datestring = (date.strftime('%Y%m%d'))

for num_runs in range(9):
	times = ["000", "012", "024", "036", "048", "060", "072", "096", "120"]
	Get_Data.get_data_https(datestring, "12", times[num_runs])
	print("Got " + times[num_runs] +"Z grib at " + str(datetime.datetime.now()))
	time.sleep(60)
