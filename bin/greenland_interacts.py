'''
An interactive map of Greenland

Datasets courtesy of: http://websrv.cs.umt.edu/isis/index.php/Main_Page

@authors Andrew Bennett, Joseph Kennedy
'''

import os, sys
import pyproj
import scipy
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap


def main(file_name='Greenland1km.nc'):
    '''Description'''

    # Set up the file and projection
    data = os.path.dirname(os.path.abspath(__file__)) + os.sep + '..' + os.sep \
            + 'data' + os.sep + file_name
    proj_file = pyproj.Proj('+proj=stere +ellps=WGS84 +datum=WGS84 +lat_ts=71.0 +lat_0=90 ' \
            + '+lon_0=321.0 +k_0=1.0')
    proj_lat_long = pyproj.Proj('+proj=latlong +ellps=WGS84 +datum=WGS84')   

    # Open up the file and grab the data we want out of it
    greenland = Dataset(data)
    x = greenland.variables['x'][:]
    y = greenland.variables['y'][:]
    nx = x.shape[0]
    ny = y.shape[0]
    y_grid, x_grid = scipy.meshgrid(y[:], x[:], indexing='ij')
    thk = greenland.variables['thk'][0]

    # Now transform the coordinates to the correct lats and lons
    lon, lat = pyproj.transform(proj_file, proj_lat_long, x_grid.flatten(), y_grid.flatten())
    lat = lat.reshape(ny,nx)
    lon = lon.reshape(ny,nx)

    # Time to put it all in the basemap
    map = Basemap(projection='stere',lat_0=65, lon_0=-25,\
                llcrnrlat=55,urcrnrlat=85,\
                llcrnrlon=-50,urcrnrlon=0,\
                rsphere=6371200.,resolution='l',area_thresh=10000)
    map.drawcoastlines(linewidth=0.25)
    map.fillcontinents(color='grey')
    map.drawmeridians(np.arange(0,360,30))
    map.drawparallels(np.arange(-90,90,30))
    x, y = map(lon,lat)


    # Now draw what we want
    cs = map.contour(x, y, thk)
    plt.show()

if __name__ == '__main__':
    '''Run the thing'''
    main()

