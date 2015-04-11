'''
An interactive map of Greenland

Datasets courtesy of: http://websrv.cs.umt.edu/isis/index.php/Main_Page

@authors Andrew Bennett, Joseph Kennedy
'''

import os, sys
import pyproj
import scipy
import mpld3
import numpy as np
import matplotlib.pyplot as plt
from mpld3 import plugins
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from interactive_legend import InteractiveLegendPlugin
from click_info import ClickInfo

def main(file_name='Greenland1km.nc'):
    '''Description'''

    # Set up the file and projection
    data = os.path.dirname(os.path.abspath(__file__)) + os.sep + '..' + os.sep \
            + 'data' + os.sep + file_name
    proj_file = pyproj.Proj('+proj=stere +ellps=WGS84 +datum=WGS84 +lat_ts=71.0 +lat_0=90 ' \
            + '+lon_0=321.0 +k_0=1.0')
    proj_lat_long = pyproj.Proj('+proj=latlong +ellps=WGS84 +datum=WGS84')
    fig, ax = plt.subplots(1,2)

    # Open up the file and grab the data we want out of it
    greenland = Dataset(data)
    x = greenland.variables['x'][:]
    y = greenland.variables['y'][:]
    nx = x.shape[0]
    ny = y.shape[0]
    y_grid, x_grid = scipy.meshgrid(y[:], x[:], indexing='ij')
    thk = greenland.variables['thk'][0]
    bheatflx = greenland.variables['bheatflx'][0]

    # Now transform the coordinates to the correct lats and lons
    lon, lat = pyproj.transform(proj_file, proj_lat_long, x_grid.flatten(), y_grid.flatten())
    lat = lat.reshape(ny,nx)
    lon = lon.reshape(ny,nx)

    # Put thickness in a basemap
    mapThk = Basemap(projection='stere',lat_0=65, lon_0=-25,\
                llcrnrlat=55,urcrnrlat=85,\
                llcrnrlon=-50,urcrnrlon=0,\
                rsphere=6371200.,resolution='l',area_thresh=10000, ax=ax[0])
    mapThk.drawcoastlines(linewidth=0.25)
    mapThk.fillcontinents(color='grey')
    mapThk.drawmeridians(np.arange(0,360,30))
    mapThk.drawparallels(np.arange(-90,90,30))
    x, y = mapThk(lon,lat)
    cs = mapThk.contour(x, y, thk, 3)

    # Put basal heat flux in a basemap
    mapFlx = Basemap(projection='stere',lat_0=65, lon_0=-25,\
                llcrnrlat=55,urcrnrlat=85,\
                llcrnrlon=-50,urcrnrlon=0,\
                rsphere=6371200.,resolution='l',area_thresh=10000, ax=ax[1])
    mapFlx.drawcoastlines(linewidth=0.25)
    mapFlx.fillcontinents(color='grey')
    mapFlx.drawmeridians(np.arange(0,360,30))
    mapFlx.drawparallels(np.arange(-90,90,30))
    x, y = mapFlx(lon,lat)
    cs = mapFlx.contour(x, y, bheatflx, 3)

    plugins.connect(fig, ClickInfo(cs))
    mpld3.show()

if __name__ == '__main__':
    '''Run the thing'''
    if len(sys.argv) > 1:
        print "loading " + sys.argv[1]
        main(sys.argv[1])
    else:
        main()
