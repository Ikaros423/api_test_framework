import pytest
import logging

from ..common.variable_handler import VariableHandler
from ..common.assertion import Assert
from ..common.file_handler import load_json_schema
from ..common.file_handler import load_yaml_data

log = logging.getLogger(__name__)

@pytest.mark.parametrize("case_data", load_yaml_data("cart/cart_cases.yaml"))
def test_cart_add(cart_api, case_data, variable_pool):
    test_name = case_data.get("test_name")
    log.info(f"[{test_name}] 测试开始")
    request_info = case_data.get("request")
    extract_info = case_data.get("extract")
    validation_info = case_data.get("validate")

    VariableHandler.substitute_variables(request_info, variable_pool)

    data = request_info.get("data", {})
    goods_data = data.get("goods_data")
    response = cart_api.add(goods_data)
    
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

    VariableHandler.extract_variables(response.json(), extract_info, variable_pool)

    log.info(f"[{test_name}] 测试结束")