import numpy as np
from scipy.interpolate import RegularGridInterpolator
from typing import List


def latlongrid(aoi_box:tuple, n_lat:int, n_lon:int)->List[np.ndarray]:
    """make a lat long regular grid in the area of interest

    Args:
        aoi_box (tuple): the aoi (box lat_max, lat_min, lon_max, lon_min)
        n_lat (int): n lattitude points in grid
        n_lon (int): n lontitude points in grid

    Returns:
        List[np.ndarray]: meshgrid (lon/lat)
    """    
    
    lat_max, lat_min, lon_max, lon_min = aoi_box
    
    lat = np.arange(lat_min, lat_max, n_lat )
    lon = np.arange(lon_min, lon_max, n_lon )
    return np.meshgrid(lon,lat)

def convert_bounds(bbox, invert_y=False):
    """
    Helper method for changing bounding box representation to leaflet notation

    ``(lon1, lat1, lon2, lat2) -> ((lat1, lon1), (lat2, lon2))``
    """
    x1, y1, x2, y2 = bbox
    if invert_y:
        y1, y2 = y2, y1
    return ((y1, x1), (y2, x2))


def reproject_data(sentinel_data):
    
    pass
    

def regrid_s2():
    
    pass