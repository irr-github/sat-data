import logging
from sentinelhub import SHConfig

from sentinel2_tests.utils.constants import SH_BASE_URL, SH_TOKEN_URL

logging.getLogger(__name__)


def setup_default_seninelhub_url():
    """setup the base URLS"""
    cfg = SHConfig.load()
    cfg.sh_base_url = SH_BASE_URL
    cfg.sh_token_url = SH_TOKEN_URL
    cfg.save()


def set_default_sentinelhub_credentials(client_id: str, client_secret: str):
    """set the default credentials for your sentinel access. This will be stored
    in the
    see https://sentinelhub-py.readthedocs.io/en/latest/configure.html

    Args:
        client_id (str): the oauth sentinel client_id
        client_secret (str): the oaut sentinel client_id
    """

    cfg = SHConfig.load()
    cfg.sh_client_id = client_id
    cfg.sh_client_secret = client_secret
    cfg.save()

    # config_location = SHConfig.get_config_location()
    # logging.info(f'{config_location=}')


def auto_setup(client_id: str, client_secret: str):
    """set the default URLS and credentials for your sentinel data access.
    The config will be stored as per https://sentinelhub-py.readthedocs.io/en/latest/configure.html

    Args:
        client_id (str): the oauth sentinel client_id
        client_secret (str): the oaut sentinel client_id
    """

    set_default_sentinelhub_credentials(client_id, client_secret)
    setup_default_seninelhub_url
