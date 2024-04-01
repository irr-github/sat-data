from sentinelhub import MosaickingOrder

# Sentinel hub links
SH_BASE_URL = "https://sh.dataspace.copernicus.eu"
SH_TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

# Mosaic
MOSAICS = {
    "newest": MosaickingOrder.MOST_RECENT,
    "oldest": MosaickingOrder.LEAST_RECENT,
    "least_cloudy": MosaickingOrder.LEAST_CC,
}

# pystac catalogues
PLANETARY_COMPUTER = "planetary"
AWS_EARTH_SEARCH_v0 = "earthsearch_v0"
AWS_EARTH_SEARCH_v1 = "earthsearch_v1"

CATALOGUES = {
    PLANETARY_COMPUTER: "https://planetarycomputer.microsoft.com/api/stac/v1/",
    AWS_EARTH_SEARCH_v0: "https://earth-search.aws.element84.com/v0",
    AWS_EARTH_SEARCH_v1: "https://earth-search.aws.element84.com/v1",
}
