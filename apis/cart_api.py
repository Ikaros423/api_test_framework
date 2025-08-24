import httpx
from .base_api import BaseAPI

class CartAPI(BaseAPI):
    """
    购物车相关API封装
    """
    
    def add(self, goods_data: str) -> httpx.Response:
        """加入购物车

        Args:
            goods_data (str): 商品编号

        Returns:
            httpx.response: _description_
        """
        url = ''
        url_params = {"s": "cart/save"}
        data_params = {"goods_data": goods_data}
        return self._request("POST", url, params=url_params, data=data_params)