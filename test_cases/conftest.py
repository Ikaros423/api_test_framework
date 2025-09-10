import pytest
import httpx
from ..apis.user_api import UserAPI
from ..apis.cart_api import CartAPI

@pytest.fixture(scope="session")
def base_url(settings):
    return settings.get('base_url')

@pytest.fixture(scope="session")
def httpx_client(base_url):
    with httpx.Client(base_url=base_url) as client:
        yield client

@pytest.fixture(scope="session")
def variable_pool():
    """
    创建一个在整个测试会话期间共享的字典，用于存储和传递变量。
    scope="session" 确保所有测试用例都使用这同一个字典。
    """
    return {}

@pytest.fixture(scope="session")
def user_api(httpx_client) -> UserAPI:
    """创建UserAPI实例

    Args:
        base_url (str): 

    Yields:
        api_instanse: UserAPI实例
    """
    api_instanse = UserAPI(httpx_client)
    return api_instanse
    
@pytest.fixture(scope="session")
def logged_in_user_api(settings, user_api) -> UserAPI:
    """创建一个登录状态的session

    Args:
        user_api (_type_): UserAPI实例
    """
    login_data = settings.get("test_account")
    # 使用user_api执行登录操作
    response = user_api.login(login_data['account'], login_data['pwd'], login_data['type'])
    
    assert response.status_code == 200
    
    # 返回该实例
    return user_api

@pytest.fixture(scope="session")
def cart_api(httpx_client, logged_in_user_api) -> CartAPI:
    """创建CartAPI实例,使用以登录的session

    Args:
        base_url (_type_): _description_
        logged_in_user_api (_type_): 获取以登录的session
    """
    # 创建CartAPI实例
    cart_instance = CartAPI(httpx_client)
    return cart_instance