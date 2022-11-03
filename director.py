import dir_fetch
from os import listdir
import time
import config

grib_files = []

grib_files = listdir(config.home_path + "/sci/data/gribs")

start_time = time.time()

# Loop through the grib files(forecast times) and generate maps for each area.
for file_name in grib_files:
    dir_fetch.main(
        file_name, 10, 60, 150, 245, "SD_N", 32.7, 242.85, 9, 160, 310, 25, 16, False
    )
    dir_fetch.main(
        file_name, 30, 45, 225, 245, "SD_wind", 32.7, 242.85, 5, 160, 310, 10, 10, True
    )
    dir_fetch.main(
        file_name, 10, 45, 280, 340, "LBI", 40.5, 360 - 73.7, 10, 80, 210, 15, 12, False
    )
    dir_fetch.main(
        file_name, -70, -10, 130, 290, "SD_S", 32.7, 242.85, 13, 160, 310, 25, 18, False
    )

end_time = time.time()
print(f"Execution time: {round(end_time-start_time, 2)}")
