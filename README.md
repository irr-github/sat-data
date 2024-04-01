# sat-data

Playground for satellite data and to assess the relative merits of the pystac/AWS and new copernicus data hub/sentinelhub api.

The project provides simple wrappers to search catalogues, download data and collate it.
This is not intended as a fully fledged project with tests but could be adapted into functional code with some refactoring. 

## sentinehub back end

The sentinelhub wrapper uses the sentinelhub package as backend and comes with functions to set your credentials and to request scripts.
The SH backend with the copernicus dataspace access is fast and automatically mosaics data. It is however, less flexible than the pystac functions.

>**NOTE**: The sentinelhub_wrapper uses the copernicus dataspace, which does not include all features (e.g. no cloud mask). It seems the paid version includes more data flags and masks. It also requires an account (see setup)

## Pystac backend
The pystac backend allows to access the aws earth-search and microsoft planetary computer data libraries, which do not require an account. Mosaicking (collating/stacking data when the AOI spans several granules or the time dimension) does not work out of the box. The wrappers here do this, as illustrated in the example.

Overall the pystac runs quite a lot slower than the SH does, even when one copies directly the microsoft git examples. 

## setup

>**IMPORTANT**: to use the sentinel hub api you will need to sign up to [the copernicus dataspace](https://dataspace.copernicus.eu/), generate oauth credentials on the [dashboard](https://shapps.dataspace.copernicus.eu/dashboard/#/account/settings) and set them up in python. Either by editing the config toml or by using the provided utils.sentinelhub_access.set_default_sentinelhub_credentials function

If you want to use as is, navigate to the folder and run:\
```pip install .sentinel2_tests_irr```\
or add the -e flag if you want to modify the code

From *vscode*, you can make a *venv* in a few clicks:\ 
- navigate to pyproject.toml or requirements.txt
- click create environment


## usage
see the example folder

## dependencies:
please check out pyproject.toml dependencies for a full list
Here are some important required packages
- sentinelhub
- pystac
- stackstac
- rasterio
- xarray
- matplotlib
- geopandas

## issues
the dynamic link between requirements.txt and pyproject.toml does not work

## TODOS
- fix projections and lat/lon plotting
- try more in depth odc.stac stac_load backend (also slow)
- try odc.alog to_rgba
