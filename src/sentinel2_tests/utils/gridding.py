from scipy.interpolate import RegularGridInterpolator
import numpy as np


def latlongrid(aoi_box:tuple, n_lat:int, n_lon:int):
    
    lat_max, lat_min, lon_max, lon_min = aoi_box
    
    lat = np.arange(lat_min, lat_max, n_lat )
    lon = np.arange(lon_min, lon_max, n_lon )
    return np.meshgrid(lon,lat)

def reproject_data(sentinel_data):
    
    
    

def regrid_s2():
    
    pass