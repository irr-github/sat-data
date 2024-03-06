# sat-data

Playground for satellite data and to assess the relative merits of the pystac/AWS-earth and new copernicus data hub/sentinelhub api 

## setup

>**IMPORTANT**: to use the sentinel hub api you will need to sign up to [the copernicus dataspace](https://dataspace.copernicus.eu/), generate oauth credentials on the [dashboard](https://shapps.dataspace.copernicus.eu/dashboard/#/account/settings) and set them up in python. Either by editing the config toml or by using the provided utils.sentinelhub_access.set_default_sentinelhub_credentials function

If you want to use as is, navigate to the folder and run:\
```pip install .sentinel2_tests_irr```\
or add the -e flag if you want to modify the code

From *vscode*, you can make a *venv* in a few clicks:\ 
- navigate to pyproject.toml or requirements.txt
- click create environment

## usage

## dependencies:
please check out pyproject.toml dependencies list or requirements.txt for a full list
Here are some important required packages
- sentinelhub
- pystac

## issues
the dynamic link between requirements.txt and pyproject.toml does not work