import pytest
import logging
from ..common.file_handler import load_yaml_data
from ..common.variable_handler import VariableHandler
from ..common.assertion import Assert
# ... 其他 imports ...

log = logging.getLogger(__name__)

# 整个流程只运行一次，所以不需要parametrize
def test_buy_product_workflow(user_api, cart_api, variable_pool):
    flow_steps = load_yaml_data("flow/buy_flow.yaml")

    for step in flow_steps:
        log.info(f"--- 开始执行流程步骤: {step['test_step']} ---")

        api = step.get('api_method')
        data = step.get('request_data')
        extract_info = step.get('extract')
        validation_info = step.get('validate')
        # 在这里实现一个更通用的步骤执行引擎
        # 1. 替换变量
        VariableHandler.substitute_variables(data, variable_pool)
        # 2. 根据api_method选择使用user_api还是cart_api
        if api == 'login':
            response = user_api.login(data.get('accounts'), data.get('pwd'), data.get('type'))
        elif api == 'add_to_cart':
            response = cart_api.add(data.get('goods_data'))
        # 3. 发送请求
        # 4. 提取变量
        VariableHandler.extract_variables(response.json(), extract_info, variable_pool)
        # 5. 断言
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
        