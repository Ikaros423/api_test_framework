import httpx
from .base_api import BaseAPI

class CartAPI(BaseAPI):
    """
    购物车相关API封装
    """
    
    async def add(self, goods_data: str, test_name: str = "N/A") -> httpx.Response:
        """加入购物车

        Args:
            goods_data (str): 商品编号

        Returns:
            httpx.response: _description_
        """
        url = ''
        url_params = {"s": "cart/save"}
        data_params = {"goods_data": goods_data}
        return await self._request("POST", url, params=url_params, data=data_params, test_name=test_name)