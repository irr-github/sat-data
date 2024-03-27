from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
from shapely import geometry

from pystac_client import ItemSearch
from typing import Tuple 
from matplotlib.figure import Figure
from xarray import DataArray

def visualise_granules_pystac(parsed_results : GeoDataFrame, query_res: ItemSearch)-> Tuple[Figure, object]:
    """plot the granules and the AOI

    Args:
        parsed_results (GeoDataFrame): the parsed results from catalogue_search.parse_results
        query_res (ItemSearch):the search results from catalogue_search.search_catalogue

    Returns:
        Tuple[Figure, object]: the fig & ax
    """    
    
    gdf = parsed_results.copy()
    gdf["granule"] = gdf["mgrs:utm_zone"].apply(lambda x: f"{x:02d}")+ gdf["mgrs:latitude_band"] + gdf["mgrs:grid_square"]
    
    fig, ax = plt.subplots(1,1)
    gdf.plot("granule",
        edgecolor="black",
        categorical=True,
        aspect="equal",
        alpha=0.2,
        figsize=(6, 12),
        # cmap = 'plasma',
        legend=True,
        legend_kwds={"loc": "upper left", "frameon": False, "ncol": 1},
        ax = ax
    )
    l = ax.get_legend()
    texts, handles = l.texts, l.legend_handles
    labels = [t.get_text() for t in texts]
    
    bbox = query_res.get_parameters()['bbox']
    box_xs, box_ys = geometry.box(*bbox).exterior.xy
    polygon = ax.fill( box_xs, box_ys, alpha = 0.75, c = 'k', label = 'AOI')

    handles.append(polygon[0])
    labels.append('AOI')

    ax.legend(handles, labels, loc = 'lower right')
    
    return fig, ax

def plot_latlon(raster_data:DataArray):
    pass
    