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
from ..utils.constants import SH_BASE_URL


def make_box_request(
    script: str,
    area_coordinates: Tuple[float],
    time_interval: Tuple[str],
    resolution_m: 60,
    config=SHConfig(),
    data_collection=DataCollection.SENTINEL2_L1C,
    crs=CRS.WGS84,
):
    """Make a request from a collection in thesentinel data catalogue based on a script

    Args:
        script (str): the scripts that sentinelhub will use to search for data
        data_collection (DataCollection): the sentinel data collection. Defaults to SENTINEL2_L1C
        time_interval (Tuple[str]): the time_interval in which the data should be searched for (yyyy-mm-dd,)
        config (object): the SHConfig. Defaults to the default config.
                        This can be set with utils.sentinelhub_access.set_default_sentinelhub_credentials
        area_coordinates (Tuple[float]): A tuple of Lon,lat,lon,lat coords defining a box
        crs (_type_, optional): _description_. Defaults to CRS.WGS84.

    Raises:
        ValueError: if data_collection is invalid

    Returns:
        _type_: _description_
    """

    # check data collection exists
    valid_collections: List[DataCollection] = DataCollection.get_available_collections()
    valid_ids = [collection.api_id for collection in valid_collections]

    if not data_collection.api_id in valid_ids:
        raise ValueError(f"Collection {data_collection.api_id} is not supported")

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
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=box_bbox,
        size=box_size,
        config=config,
    )

    return request
