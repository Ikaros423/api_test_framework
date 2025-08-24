import pytest
from ..apis.login_api import LoginAPI

@pytest.fixture(scope="session")
def base_url(settings):
    return settings.get('base_url')

@pytest.fixture(scope="session")
def login_api(base_url, token = None):
    """创建LoginAPI实例

    Args:
        base_url (str): 
        token (str, optional): Defaults to None.

    Yields:
        api_instanse: LoginAPI实例
    """
    api_instanse = LoginAPI(base_url, token)
    yield api_instanse
    api_instanse.close()