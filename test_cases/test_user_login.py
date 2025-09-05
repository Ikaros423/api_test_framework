from ..common.file_handler import load_yaml_data
from ..common.file_handler import load_json_schema
from ..common.assertion import Assert
import pytest
import logging

log = logging.getLogger(__name__)

@pytest.mark.parametrize("case_data", load_yaml_data("user/login_cases.yaml"))
def test_user_login(user_api, case_data):
    test_name = case_data.get("test_name")
    log.info(f"[{test_name}] 测试开始")
    request_info = case_data.get("request")
    validation_info = case_data.get("validate")

    data = request_info.get("data", {})
    accounts = data.get("accounts")
    pwd = data.get("pwd")
    type = data.get("type")
    
    response = user_api.login(accounts, pwd, type)
    
    # 初始化断言对象
    asserter = Assert(response)
    
    if validation_info:
        for validation_rule in validation_info:
            validation_type = validation_rule.get("type")
            expected = validation_rule.get("expected")
            
            if validation_type == "status_code":
                asserter.stauts_code_is(expected)
                
            elif validation_type == "json_path":
                path = validation_rule.get("path")
                asserter.json_path_value_is(path, expected)
                
            elif validation_type == "schema":
                schema_path = validation_rule.get("path")
                schema_data = load_json_schema(schema_path)
                asserter.validate_with_schema(schema_data)
                
    log.info(f"[{test_name}] 测试结束")