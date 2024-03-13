import geopandas as gpd
from pystac_client import Client, ItemSearch
import shapely
from sentinel2_tests.utils.constants import CATALOGUES, AWS_EARTH_SEARCH_v0, AWS_EARTH_SEARCH_v1, PLANETARY_COMPUTER

def search_catalogue(aoi_bbox:tuple, catalogue = CATALOGUES[PLANETARY_COMPUTER], cloud_cover_limit = None, collections = ["sentinel-2-l2a"], date_range = ("2021-09-16","2021-10-16"), max_results = None)-> ItemSearch:
    """search the relevant catalogue (designed for s2-l2a but other data sources will work)

    Args:
        aoi_bbox (tuple): the bbox defining the area of interest
        catalogue (_type_, optional): The catalogue url. Defaults to CATALOGUES[PLANETARY_COMPUTER].
        cloud_cover_limit (float, optional): The max cloud fraction. Defaults to None (no filter).
        collections (list, optional): the collections to search. Defaults to ["sentinel-2-l2a"].
        date_range (tuple, optional): the date range as tuple or date as str, can also be None. Defaults to ("2021-09-16","2021-10-16").
        max_results (int, optional): the max number of results to return. Defaults to None.

    Raises:
        ValueError: Catalogue not supported (not in constnts.CATALOGUES)

    Returns:
        pystac_client.ItemSearch: the pystac query result
    """    
    if catalogue not in CATALOGUES.values():
        raise ValueError(f'Unsupported Catalogue {catalogue} not in {list(CATALOGUES.values())}')
    
    catalog = Client.open(catalogue)
    if catalogue == CATALOGUES[AWS_EARTH_SEARCH_v0]:
        catalog.add_conforms_to('ITEM_SEARCH')
    
    for collection in collections:
        check_collection_in_catalogue(catalog, collection)
        
    if cloud_cover_limit:
        query_terms = {'eo:cloud_cover': {'lt': cloud_cover_limit*100}}
    else:
        query_terms = None
        
    query = catalog.search(
        collections=collections, datetime=date_range, limit=max_results, bbox=aoi_bbox, query = query_terms,
    )
    
    return query
    
def check_collection_in_catalogue(catalog:str, collection:str):
    """check that the requested collection (eg sentinel-2-l2a) is part of the catalogue

    Args:
        catalog (str - url): the catalogue
        collection (str): the requested data collection

    Raises:
        ValueError: collection is not available
    """    
    
    # if not catalog.url in CATALOGUES.values():
    #     raise ValueError(f'unsupported catalogue {catalog} not in {CATALOGUES}')
        
    available_collections = [c.id for c in catalog.get_all_collections()]
    
    if not collection in available_collections:
        msg = "\n\t".join(available_collections)
        raise ValueError(f"Collection  {collection} is not in the search catalogue. Available: \n\t{msg}")

    return True
    
def parse_results(query: ItemSearch)->gpd.GeoDataFrame:
    """parse results into a geopandas DataFrame

    Args:
        query (ItemSearch): the search_catalogue result
    Raises:
        ValueError: if no results were found

    Returns:
        gpd.GeoDataFrame: the results ranked by aoi coverage
    """    
    
    collection = query.item_collection()
    if len(collection)==0:
        raise ValueError('No results found')
    
    # add the assests & the id to the feature collection
    for c in collection:
        c.properties['id']=c.id
        c.properties['assets'] = c.assets
        
    results_gdf = gpd.GeoDataFrame.from_features(collection)
    aoi = shapely.geometry.box(*query.get_parameters()['bbox'])
    aoi_frac = lambda geo: shapely.intersection(geo, aoi).area/aoi.area
    results_gdf['aoi_fraction'] = results_gdf['geometry'].apply(aoi_frac)
    
    return results_gdf.sort_values('aoi_fraction', ascending=False)

def collate_results():
    
    pass