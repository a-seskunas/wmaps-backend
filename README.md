 Wmaps

Wmaps is a Python application that produces maps to show the directed wind fetch for a particular location.    

[https://www.wmaps.net](https://www.wmaps.net)

## Motivation

There's plenty of resources on the internet to get wind forecast information.  Most of it is derived from the GFS weather model.  The problem with all of the GFS derived wind maps that I've seen, is that they show too much information to be easily useful for a swell forecast. So I decided to make my own maps, using the publicly available data from the GFS weather model. Using a wmaps forecast map, you can quickly determine if there's going to be a swell for a given location.


## Description

  * Wmaps pulls weather data from the NOAA NOMAD project here [wmaps-backend/data](https://github.com/a-seskunas/wmaps-backend/tree/main/data).   
  * The data is then processed, filtered and made into a maps here [wmaps-backend/dir_fetch.py](https://github.com/a-seskunas/wmaps-backend/blob/main/dir_fetch.py).   
  * A 0Z and 12Z map are archived each day here [wmaps-backend/namer.py](https://github.com/a-seskunas/wmaps-backend/blob/main/namer.py).    
  * After the data has been processed and made into maps, the maps are made available to a Flask web app which displays them on the wmaps website.



## Use

Lets look at an example map.   
![](https://github.com/a-seskunas/wmaps-backend/blob/main/examples/fetch-example.png?raw=true)    

We've got a good looking fetch circled in red here.  Note the direction of the arrows, pointing in the general direction of the West Coast of America, where we're located.  Also note that the wind data is filtered to show only wind that is traveling towards the maps destination.     

So now we have a fetch of wind pointing in the correct direction to give us some swell at our destination, which is, in this case San Diego, CA.  The next piece of information a wmap gives us is roughly how many days until a swell from a given fetch will arrive.

![](https://github.com/a-seskunas/wmaps-backend/blob/main/examples/days-example.png?raw=true)

The vertical curved lines drawn on the map trace out equal distances from the maps destination.  The distances drawn on the map make some assumptions about the fetch generating the swell, so they are meant to be a rough guide to when a swell will arrive.  So in this case, the swell will take approximately 4 days to reach San Diego.   

![](https://github.com/a-seskunas/wmaps-backend/blob/main/examples/dir-example.png?raw=true)


The horizontal curved lines drawn on the map are great circle lines.  Great circle lines are the path a swell(or a plane flying) will take across the earth.  On a wmap they show the angle of an incoming swell.  Swell angles are important when figuring out how big, or even whether a swell will reach a certain area.  In this example, most of the swell above 300° won't get into San Diego.

![](https://github.com/a-seskunas/wmaps-backend/blob/main/examples/date-example.png?raw=true)

Last of all each map has two dates labeled on it.  The first date comes directly from the GFS grib file and indicates the model run date.  The second date is the date the wmaps python application processed the GFS grib file.  A key thing to note is that the days of the month should match i.e. the wmaps application should be processing a current grib file.   There are occasional issues with the NOAA nomad project and sometimes the GFS data isn't updated on time.  

## Contributing

As of now this is a personal project.

## License

[MIT](https://choosealicense.com/licenses/mit/)
