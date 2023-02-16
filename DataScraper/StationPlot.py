#import geoplot.crs as crs
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

import pandas as pd

# call country shapefiles
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# get the station data ready for plottin'
stations = pd.read_csv('/home/snowdaere/PythonProjects/firecast/DataScraper/StationLookup.csv')
stations = gpd.GeoDataFrame(stations, geometry=[Point(xy) for xy in zip(stations.lon, stations.lat)])

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(100, 100))

# plot world map
world.plot(ax=ax1, edgecolor='black', facecolor='white')
stations.plot(ax=ax1, markersize=0.1)

# plot US map

fig.savefig('Plots/WorldMap.png')
