import numpy as np
import stackstac

from rioxarray import open_rasterio
from geopandas import GeoDataFrame
from typing import List
from pystac_client import Client, ItemSearch

from sentinel2_tests.utils.constants import CATALOGUES, AWS_EARTH_SEARCH_v0, AWS_EARTH_SEARCH_v1, PLANETARY_COMPUTER

def download_top_result(gdf_results:GeoDataFrame, query:ItemSearch, band:str, rank_by = ['aoi_fraction']):
    """get the top result from the query search results

    Args:
        gdf_results (GeoDataFrame): the geodataframe containing the features
        query (ItemSearch): the pystack query result (catalog_search.search_catalogue)
        band (str): the asset to be fetched
        rank_by (list, optional): the colum(s) to use for ranking results. Defaults to ['aoi_fraction'].

    Returns:
        rioxarray: the band
    """    
    
    # sort the data
    gdf = gdf_results.copy()
    gdf.sort_values(by = rank_by, ascending=False, inplace=True)
    # get the best result's index in the collection
    item_idx = gdf.reset_index().loc[0]['index']
    itm = [itm for itm in query.items()][item_idx]

    # download the data
    return open_rasterio(itm.assets[band].get_absolute_href())

def fetch_aoi_data(granule_list:List[GeoDataFrame], query_results:ItemSearch,asset_names: List[str], resolution = None ,  limit_to_bbox = True ):
    """download and combine the data.
       To get vis data, download the RGB bands and combine them with the process_data tools

    Args:
        granule_list (List[GeoDataFrame]): the list of granule metadata that covers the AOI (from catalogue_search.get_aoi_granules)
        query_results (ItemSearch): the pystac query result
        asset_name (str): the asset to fetch
    Returns:
        DataArray: the time stackstac combined arrays (time, band)
    """    
  
    
    # granule list is a list of geoSeries
    if limit_to_bbox:
        bbox = query_results.get_parameters()['bbox']
    else:
        bbox = None
    indices  = [geo_ser.query_index for geo_ser in granule_list]
    items = [itm for i,itm in enumerate(query_results.items()) if i in indices ]

    # find the lowest res - THIS MAY NOT BE COMPATIBLE WITH EARTHSEARCH V0
    if resolution is None:
        gsds = []
        for gdf in granule_list:
            for band in asset_names:
                gsds.append(gdf.assets[band].extra_fields['gsd'])
        resolution = max(gsds)
        
    data = (
    stackstac.stack(
        items,
        assets=asset_names,  # red, green, blue
        chunksize=4096,
        resolution=resolution,
        bounds_latlon = bbox
    )
    .where(lambda x: x > 0, other=np.nan)  # sentinel-2 uses 0 as nodata
    # .assign_coords(band=lambda x: x.common_name.rename("band"))  # use common names
    )
    
    return data
