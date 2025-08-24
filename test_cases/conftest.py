import pytest
from ..apis.user_api import UserAPI
from ..apis.cart_api import CartAPI

@pytest.fixture(scope="session")
def base_url(settings):
    return settings.get('base_url')

@pytest.fixture(scope="session")
def user_api(base_url):
    """创建UserAPI实例

    Args:
        base_url (str): 

    Yields:
        api_instanse: UserAPI实例
    """
    api_instanse = UserAPI(base_url)
    yield api_instanse
    api_instanse.close()
    
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
def cart_api(base_url, logged_in_user_api):
    """创建CartAPI实例,使用以登录的session

    Args:
        base_url (_type_): _description_
        logged_in_user_api (_type_): 获取以登录的session
    """
    # 创建CartAPI实例, 并将以登录的session传递给它
    cart_instance = CartAPI(base_url)
    cart_instance.session = logged_in_user_api.session
    yield cart_instance
    cart_instance.close()