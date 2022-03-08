import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
import numpy as np

import matplotlib as matplotlib
# Use Agg so we can save the map without a display
matplotlib.use("Agg")

import pygrib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import math as math
import g_circ as gc
import datetime
import image_to_db as to_db
import sqlite3
import pickle




def main(
    file_name,
    lat1,
    lat2,
    lon1,
    lon2,
    home_name,
    home_lat,
    home_lon,
    days,
    angle_start,
    angle_stop,
    wind_thresh,
    wave_period,
    thin_out,
):



    with open("/home/adam/sci/basemaps/" + home_name + "_base.pkl", "rb") as infile:
        ax = pickle.load(infile)

    grbs = pygrib.open("/home/adam/sci/data/gribs/" + str(file_name))

    grb = grbs.select(name="10 metre U wind component")[0]
    U, lat, lon = grb.data(lat1, lat2, lon1, lon2 + 5)

    grb = grbs.select(name="10 metre V wind component")[0]
    V, lat, lon = grb.data(lat1, lat2, lon1, lon2 + 5)

    grb = grbs.message(1)
    pressure, lat, lon = grb.data(lat1, lat2, lon1, lon2 + 5)
    pressure = pressure / 100

    X = 30
    C = "grey"
    circle_length = math.radians(lon2 - lon1)

    gcs, angles = gc.draw_lines(
        [home_lat, home_lon], angle_start, angle_stop, circle_length
    )

    magnitude = (
        U**2 + V**2
    ) ** 0.5 * 1.944  # convert U,V components to speed in knots

    # Calculate the vector directions that point toward the home lat/lon
    HOME = [home_lat, home_lon]
    home_lats = np.ones(np.shape(lat))
    home_lons = np.ones(np.shape(lon))

    home_lats = home_lats * HOME[0]
    home_lons = home_lons * HOME[1]

    home_vectors = gc.get_g_circ_bearing(home_lats, 360 - home_lons, lat, 360 - lon)

    # Convert U and V wind components to wind direction
    wind_dir = 90.0 - (
        np.arctan2((V / magnitude), (U / magnitude)) * 180.0 / math.pi + 180.0
    )
    # Get rid of negative wind directions.
    wind_dir[wind_dir < 0] = 360 + wind_dir[wind_dir < 0]

    # strip out any wind vectors that are pointing in the wrong direction
    # i.e. we only want to view vectors pointing towards the home lat/lon
    msk = abs(home_vectors - wind_dir) > 40
    U[msk] = None
    V[msk] = None
    magnitude[msk] = None

    # do the same as above with the magnitude
    wind_msk = magnitude < wind_thresh
    U[wind_msk] = None
    V[wind_msk] = None
    magnitude[wind_msk] = None

    ############################
    # Thin out data points for wind arrows if needed
    if thin_out:
        yy = np.arange(0, lon.shape[0], 1)
        xx = np.arange(0, lat.shape[1], 1)

    else:
        yy = np.arange(0, lon.shape[0], 4)
        xx = np.arange(0, lat.shape[1], 4)

    points = np.meshgrid(yy, xx)
    points = tuple(
        points
    )  

    wind_levels = np.arange(wind_thresh - 5, wind_thresh + 50, 5)

    pressure_levels = np.arange(950, 1032, 2)
    pressure_contour = ax.contour(
        lon,
        lat,
        pressure,
        transform=ccrs.PlateCarree(),
        levels=pressure_levels,
        zorder=6,
        colors="grey",
    )
    plt.clabel(pressure_contour, inline=True, fontsize=12, fmt="%1i")
    wind_contour = ax.contourf(
        lon, lat, magnitude, transform=ccrs.PlateCarree(), levels=wind_levels, zorder=4
    )
    ax.quiver(
        lon[points],
        lat[points],
        U[points],
        V[points],
        transform=ccrs.PlateCarree(),
        zorder=5,
    )
    color_bar = plt.colorbar(wind_contour, shrink=0.9, pad=0.05)

    now = datetime.datetime.now()

    fig1 = plt.gcf()
    # Get title for chart
    grbs.seek(0)
    title = str(grbs.read(1)[0])
    print(title)
    title = title.split(":")
    plt.title(
        title[6]
        + " "
        + title[7]
        + ",  compiled on "
        + now.strftime("%b %d %H:%M")
        + " UTC"
    )
    # fig1.tight_layout()
    forecast_hour = title[6][10:13].rstrip("h")
    forecast_hour = forecast_hour.strip()
    fig1.savefig(
        "/var/www/html/images/"
        + home_name
        + "surface_pressure"
        + forecast_hour
        + ".png",
        dpi=80,
        pad_inches=0.3,
        bbox_inches="tight",
    )
    # save 00Z image in the past images folder for long term storage
    if forecast_hour == "0":
        path_to_past_image = (
            "/var/www/html/images/past_images/"
            + home_name
            + now.strftime("%Y-%m-%d_%H")
            + ".png"
        )
        fig1.savefig(path_to_past_image, dpi=60, pad_inches=0.3, bbox_inches="tight")

        # add path to the image to the database
        conn = sqlite3.connect("/home/adam/sci/db/image_paths.db")
        with conn:
            im_name = home_name + now.strftime("%Y-%m-%d_%H") + ".png"
            image = (
                path_to_past_image,
                now.strftime("%Y-%m-%d"),
                now.strftime("%H"),
                home_name,
                im_name,
            )
            image_id = to_db.create_image(conn, image)
    plt.close("all")
    print(
        "png saved at /var/www/html/images/ at "
        + "{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
    )


if __name__ == "__main__":
    main(*sys.argv)


