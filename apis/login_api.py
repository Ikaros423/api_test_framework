import httpx
from .base_api import BaseAPI

class LoginAPI(BaseAPI):
    """
    登录相关的API封装
    """
    def login(self, accounts: str, pwd: str, type: str) -> 'httpx.Response':
        """登录

        Args:
            accounts (str): 账号
            pwd (str): 密码
            type (str): 登录方式(账号、手机、邮箱)

        Returns:
            httpx.Response: 响应对象
        """
        url = ''
        url_params = {"s": 'user/login'}
        login_form_data = {"accounts": accounts,
                           "pwd": pwd,
                           "type": type
                           }
        return self.request('POST', url, params=url_params, data=login_form_data)
        