import re
import logging
from jsonpath import JSONPath

log = logging.getLogger(__name__)

class VariableHandler:
    # 定义变量的正则表达式,匹配 ${variable_name} 格式
    _VAR_REGEX = re.compile(r"\$\{([^}]+)\}")
    
    @classmethod
    def extract_variables(cls, response_data: dict, extract_rules: list, pool: dict):
        """根据提取规则,从响应数据中提取变量并存入池中

        Args:
            response_data (dict): API响应的json字典
            extract_rules (list): yaml中定义的提取规则列表
            pool (dict): 全局变量池字典
        """
        if not extract_rules:
            return
        
        for rule in extract_rules:
            var_name = rule.get('var_name')
            json_path = rule.get('json_path')
            
            if not (var_name and json_path):
                continue
            
            matches = JSONPath(json_path).search(response_data)
            if matches:
                extracted_value = matches[0]
                log.info(f"提取变量: '{var_name}' = '{extracted_value}'")
                pool[var_name] = extracted_value
            else:
                log.warning(f"未能从响应中提取变量 '{var_name}', JSONpath: '{json_path}' 未匹配到值")
                
    
    @classmethod
    def substitute_variables(cls, data_structrue, pool: dict):
        """递归地替换数据结构（字典或列表）中所有匹配 `${...}` 格式的字符串

        Args:
            data_structrue (_type_): 包含待替换变量的请求数据（如 a dict for headers/data）
            pool (dict): 全局变量池字典
        """
        if isinstance(data_structrue, dict):
            for key, value in data_structrue.items():
                data_structrue[key] = cls.substitute_variables(value, pool)
        elif isinstance(data_structrue, list):
            for i, item in enumerate(data_structrue):
                data_structrue[i] = cls.substitute_variables(item, pool)
        elif isinstance(data_structrue, str):
            # 找到所有匹配的变量
            matches = cls._VAR_REGEX.findall(data_structrue)
            for var_name in matches:
                if var_name in pool:
                    placeholder = f"${{{var_name}}}"
                    data_structrue = data_structrue.replace(placeholder, str(pool[var_name]))
                    log.info(f"替换变量 '{placeholder}' -> '{pool[var_name]}'")
            
        return data_structrue