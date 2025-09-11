import pytest
from ..common.file_handler import load_yaml_data
from ..common.file_handler import load_json_schema
from ..common.assertion import Assert
import logging
import allure
import asyncio

log = logging.getLogger(__name__)

case_data = load_yaml_data("user/login_cases.yaml")

@pytest.mark.asyncio
@pytest.mark.parametrize("case", load_yaml_data("user/login_cases.yaml"))
async def test_user_login(user_api, case):
    test_name = case.get("test_name")
    log.info(f"[{test_name}] 测试开始")
    request_info = case.get("request", {})
    validation_info = case.get("validate")

    data = request_info.get("data", {})
    accounts = data.get("accounts")
    pwd = data.get("pwd")
    type = data.get("type")
    
    response = await user_api.login(accounts, pwd, type, test_name)
    
    # 初始化断言对象
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
                
    log.info(f"[{test_name}] 测试结束")

# async def test_user_login(user_api, case_data):
#     # 封装每个并发任务
#     async def make_request(case):
#         test_name = case.get("test_name")
#         with allure.step(f"{test_name}"):
#             log.info(f"[{test_name}] 测试开始")
#             request_info = case.get("request", {})
#             validation_info = case.get("validate")

#             data = request_info.get("data", {})
#             accounts = data.get("accounts")
#             pwd = data.get("pwd")
#             type = data.get("type")
            
#             response = await user_api.login(accounts, pwd, type, test_name)
            
#             # 初始化断言对象
#             asserter = Assert(response)
            
#             if validation_info:
#                 for validation_rule in validation_info:
#                     validation_type = validation_rule.get("type")
#                     expected = validation_rule.get("expected")
                    
#                     if validation_type == "status_code":
#                         asserter.status_code_is(expected)
                        
#                     elif validation_type == "json_path":
#                         path = validation_rule.get("path")
#                         asserter.json_path_value_is(path, expected)
                        
#                     elif validation_type == "schema":
#                         schema_path = validation_rule.get("path")
#                         schema_data = load_json_schema(schema_path)
#                         asserter.validate_with_schema(schema_data)
                        
#             log.info(f"[{test_name}] 测试结束")
            
#     # 创建并并发执行这些封装好的任务
#     tasks = [make_request(case) for case in case_data]
    
#     # 使用 asyncio.gather 来运行，并设置 return_exceptions=True
#     # 这样即使某个任务失败，也不会中断其他任务
#     results = await asyncio.gather(*tasks, return_exceptions=True)
    
#     # 检查是否有异常发生，如果有，则重新抛出，让pytest知道测试失败了
#     for result in results:
#         if isinstance(result, Exception):
#             raise result