from http.client import LOOP_DETECTED
import pytest
import asyncio
import logging
from ..common.file_handler import load_yaml_data, load_json_schema
from ..common.assertion import Assert
from ..apis.user_api import UserAPI

log = logging.getLogger(__name__)

# 我们需要一个未登录的 user_api 实例
@pytest.fixture(scope="session")
def guest_user_api(httpx_client) -> UserAPI:
    return UserAPI(httpx_client)

@pytest.mark.asyncio(loop_scope="session")
async def test_all_login_scenarios_concurrently(guest_user_api):
    """
    并发地测试所有登录场景
    """
    # 1. 加载所有测试用例数据
    all_cases = load_yaml_data("user/login_cases.yaml")

    # 封装每个并发任务的协程
    async def run_single_login_case(case_data):
        test_name = case_data.get("test_name")
        request_info = case_data.get("request", {})
        validation_info = case_data.get("validate")
        
        data = request_info.get("data", {})
        accounts = data.get("accounts")
        pwd = data.get("pwd")
        req_type = data.get("type")

        log.info(f"[{test_name}] 并发任务开始")
        response = await guest_user_api.login(accounts, pwd, req_type, test_name)

        # 如果返回 500，记录详细信息以便排查
        if response.status_code >= 500:
            log.error("[%s] 服务器 5xx 响应: status=%s body=%s", test_name, response.status_code, await response.aread() if hasattr(response, "aread") else response.text)

        # 在协程内部直接进行断言
        asserter = Assert(response)
        if validation_info:
            for validation_rule in validation_info:
                validation_type = validation_rule.get("type")
                expected = validation_rule.get("expected")
                
                if validation_type == "status_code":
                    asserter.status_code_is(expected)
                    
                elif validation_type == "json_path":
                    path = validation_rule.get("path")
                    asserter.json_path_value_is(path, expected)
                    
                elif validation_type == "schema":
                    schema_path = validation_rule.get("path")
                    schema_data = load_json_schema(schema_path)
                    asserter.validate_with_schema(schema_data)
        log.info(f"[{test_name}] 并发任务结束")

    # 2. 【扇出】创建所有任务
    tasks = [run_single_login_case(case) for case in all_cases]

    # 3. 【扇入】并发执行所有任务
    # 使用 asyncio.gather 来运行，并设置 return_exceptions=True
    # 这样即使某个任务失败，也不会中断其他任务
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 4. 检查是否有异常发生，如果有，则重新抛出，让pytest知道测试失败了
    # 这是确保即使在并发中，测试失败也能被正确报告的关键
    for result in results:
        if isinstance(result, Exception):
            # 打印详细的异常信息，方便调试
            log.error(f"并发测试中出现异常: {result}")
            raise result