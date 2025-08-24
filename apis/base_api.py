import httpx
# from common.logger import logger # 假设你有一个日志模块

class BaseAPI:
    def __init__(self, base_url: str):
        """初始化BaseAPI

        Args:
            base_url (str): 目标环境的基础URL
            token (str, optional): 登录后获取的认证token. Defaults to None.
        """
        self.base_url = base_url
        self.session = httpx.Client() # 使用Client可以保持会话和cookies

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """封装一个通用的请求方法

        Args:
            method (str): 请求方法 (GET, POST, PUT, etc.)
            url (str): API的路径 (e.g., /products/123)
            kwargs: 其他httpx支持的参数 (e.g., json, data, params)
        Returns:
            httpx.Response: httpx.Response 对象
        """
        full_url = self.base_url.rstrip('/') + '/' + url.lstrip('/')
        
        # logger.info(f"发起请求: {method} {full_url}")
        # logger.info(f"请求参数: {kwargs}")
        
        try:
            response = self.session.request(method, full_url, **kwargs)
            response.raise_for_status() # 如果是4xx或5xx状态码，则抛出异常
            # logger.info(f"响应状态码: {response.status_code}")
            # logger.info(f"响应内容: {response.text[:500]}...") # 只记录部分响应
            return response
        except httpx.HTTPStatusError as e:
            # logger.error(f"请求失败: {e.response.status_code} - {e.response.text}")
            raise # 重新抛出异常，让pytest能捕获到失败
        except Exception as e:
            # logger.error(f"发生未知错误: {e}")
            raise

    def close(self):
        """关闭session"""
        self.session.close()