from aenum import constant
from sentinelhub import (
    CRS,
    BBox,
    SHConfig,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
)
from typing import List, Tuple
from ..utils.constants import SH_BASE_URL, MOSAICS


def make_box_request(
    script: str,
    area_coordinates: Tuple[float],
    time_interval: Tuple[str],
    resolution_m=60,
    max_could_frac=None,
    config=SHConfig(),
    data_collection=DataCollection.SENTINEL2_L1C,
    mosaic_order: constant = MOSAICS["least_cloudy"],
    crs=CRS.WGS84,
):
    """Make a request from a collection in thesentinel data catalogue based on a script.
    This automatically mosaics the data.

    Args:
        script (str): the scripts that sentinelhub will use to search for data
        data_collection (DataCollection): the sentinel data collection. Defaults to SENTINEL2_L1C
        time_interval (Tuple[str]): the time_interval in which the data should be searched for (yyyy-mm-dd,)
        resolution_m (int): the resolution in m. Defaults to 60 (lowest - swir16)
        max_could_frac (float): the max cloud fraction. default =0.2
        config (object): the SHConfig. Defaults to the default config.
                        This can be set with utils.sentinelhub_access.set_default_sentinelhub_credentials
        area_coordinates (Tuple[float]): A tuple of Lon,lat,lon,lat coords defining a box
        mosaic_order (constant): the mosaicing order, see constants.MOSAICS. Defaults to least cloudy
        crs (_type_, optional): the CRS. Defaults to CRS.WGS84.

    Raises:
        ValueError: if data_collection is invalid
        ValueError: if mosaic_order is invalid
    Returns:
        SentinelHubRequest: the request result
    """

    # check data collection exists
    valid_collections: List[DataCollection] = DataCollection.get_available_collections()
    valid_ids = [collection.api_id for collection in valid_collections]

    if not data_collection.api_id in valid_ids:
        raise ValueError(f"Collection {data_collection.api_id} is not supported")
    if not mosaic_order in MOSAICS.values():
        raise ValueError(f"invalid mosaicing order: valid are {MOSAICS}")

    # set data source to match config
    data_collection.service_url = config.sh_base_url

    # make box
    box_bbox = BBox(bbox=area_coordinates, crs=crs)
    box_size = bbox_to_dimensions(box_bbox, resolution=resolution_m)

    request = SentinelHubRequest(
        evalscript=script,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=data_collection,
                time_interval=time_interval,
                maxcc=max_could_frac,
                mosaicking_order=mosaic_order,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=box_bbox,
        size=box_size,
        config=config,
    )

    return request
