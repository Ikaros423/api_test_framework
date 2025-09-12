import httpx
import logging
import allure
import json

# 获取当前模块名命名的log实例
log = logging.getLogger(__name__)

class BaseAPI:
    def __init__( self, session: httpx.AsyncClient):
        """初始化BaseAPI

        Args:
            session (httpx.AsyncClient): httpx.AsyncClient实例
        """
        self.session = session # 使用Client可以保持会话和cookies

    async def _request(self, method: str, url: str, test_name: str = "N/A", **kwargs) -> httpx.Response:
        """封装一个通用的异步请求方法

        Args:
            method (str): 请求方法 (GET, POST, PUT, etc.)
            url (str): API的路径 (e.g., /products/123)
            kwargs: 其他httpx支持的参数 (e.g., json, data, params)
        Returns:
            httpx.Response: httpx.Response 对象
        """
        log.info(f"[REQ-ID: {test_name}] 发起异步请求: {method} {url}")
        log.debug(f"[REQ-ID: {test_name}] 请求参数: {kwargs}")
        
        # --- Allure 集成：准备附件内容 ---
        # request_details = (
        #     f"--> {method.upper()} {url}\n"
        #     f"--> Headers: {self.session.headers}\n"
        #     f"--> Params: {kwargs.get('params')}\n"
        #     f"--> Data: {kwargs.get('data')}\n"
        #     f"--> JSON: {kwargs.get('json')}\n"
        # )
        # # 将请求详情附加到当前Allure Step中
        # allure.attach(request_details, name=f"Request Details [{test_name}]", attachment_type=allure.attachment_type.TEXT)

        try:
            response = await self.session.request(method, url, **kwargs)
            
            # --- Allure 集成：准备响应附件 ---
            # response_headers = json.dumps(dict(response.headers), indent=2, ensure_ascii=False)
            # response_body = response.text
            # try: # 尝试格式化JSON响应体
            #     response_body_json = json.dumps(response.json(), indent=2, ensure_ascii=False)
            #     allure.attach(response_body_json, name=f"Response Body (JSON) [{test_name}]", attachment_type=allure.attachment_type.JSON)
            # except json.JSONDecodeError:
            #     allure.attach(response_body, name=f"Response Body (Text) [{test_name}]", attachment_type=allure.attachment_type.TEXT)

            # allure.attach(response_headers, name=f"Response Headers [{test_name}]", attachment_type=allure.attachment_type.JSON)
            
            response.raise_for_status() # 如果是4xx或5xx状态码，则抛出异常
            log.info(f"[REQ-ID: {test_name}] 响应状态码: {response.status_code}")
            log.debug(f"[REQ-ID: {test_name}] 响应内容: {response.text[:500]}...") # 只记录部分响应
            return response
        except httpx.HTTPStatusError as e:
            log.error(f"[REQ-ID: {test_name}] 请求失败: {e.response.status_code} - {e.response.text}", exc_info=True)
            # allure.attach(f"请求失败: {e.response.status_code}\n{e.response.text}", name=f"Request Failed [{test_name}]", attachment_type=allure.attachment_type.TEXT)
            raise # 重新抛出异常，让pytest能捕获到失败
        except Exception as e:
            log.error(f"[REQ-ID: {test_name}] 发生未知错误: {e}", exc_info=True)
            # allure.attach(f"发生未知错误: {e}", name=f"Unknown Error [{test_name}]", attachment_type=allure.attachment_type.TEXT)
            raise