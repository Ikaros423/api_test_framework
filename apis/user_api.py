import httpx
from .base_api import BaseAPI

class UserAPI(BaseAPI):
    """
    用户相关的API封装
    """
    async def login(self, accounts: str, pwd: str, type: str, test_name: str = "N/A") -> 'httpx.Response':
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
        return await self._request('POST', url, params=url_params, data=login_form_data, test_name=test_name)