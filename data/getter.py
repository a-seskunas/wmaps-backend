# Gets grib files via get_data for each forecast hour.

# Needs to be run with a model run argument from the command line.
# The get_data file has the https call and the saves the grib
# file to the appropriate place.

import get_data as Get_Data
from datetime import datetime
from time import sleep
import argparse


def main():
    timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    forecast_hours = ["000", "012", "024", "036", "048", "060", "072", "096", "120"]

    datestring = datetime.today().strftime("%Y%m%d")

    # Set up command line argument for the model run hour
    parser = argparse.ArgumentParser()
    parser.add_argument("-Z", type=str, help="Model run hour, i.e. 00 or 12")
    args = parser.parse_args()

    for hour in forecast_hours:
        Get_Data.get_data_https(datestring, args.Z, hour)
        print("Got " + hour + "Z grib at " + timestamp)
        sleep(60)


if __name__ == "__main__":
    main()
