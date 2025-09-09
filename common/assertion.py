import httpx
import json
from jsonpath import JSONPath 
from jsonschema import validate, ValidationError

class Assert:
    def __init__(self, response: httpx.Response) -> None:
        """初始化断言对象

        Args:
            response (httpx.Response): httpx响应对象
        """
        self.response = response
        try:
            self.json_data = response.json()
        except Exception:
            self.json_data = None
            
    def status_code_is(self, expected_code: int):
        """断言HTTP状态码

        Args:
            expected_code (int): 预期状态码
        """
        actual_code = self.response.status_code
        assert actual_code == expected_code, \
            f'状态码校验失败! 预期: {expected_code}, 实际: {actual_code}, 响应: {self.response.text[:200]}'
        return self
            
    def contain_text(self, expected_text: str):
        """断言响应文本中包含指定字符串

        Args:
            expected_text (str): 预期字符串
        """
        assert expected_text in self.response.text, \
            f"文本内容校验失败! 未找到预期文本: '{expected_text}'"
        return self         
    
    def json_path_exists(self, json_path: str):
        """断言响应JSON中, 存在json_path表达式匹配的结果

        Args:
            json_path (str): jsonpath表达式
        """
        if self.json_data == None:
            raise AssertionError("响应体不是有效的SON格式")
        
        matches = JSONPath(json_path).search(self.json_data)
        assert len(matches) > 0, f"JSONPath '{json_path}'未找到匹配项"
        return self
    
    def json_path_value_is(self, json_path: str, expected_value):
        """断言响应JSON中,通过json_path获取的值等于预期值

        Args:
            json_path (str): jsonpath表达式
            expected_value (_type_): 预期值
        """
        if self.json_data == None:
            raise AssertionError("响应体不是有效JSON格式")
        
        matches = JSONPath(json_path).search(self.json_data)
        actual_value = matches[0]
        assert actual_value == expected_value, \
            f"JSON值校验失败! 路径: '{json_path}', 预期: '{expected_value}', 实际: '{actual_value}'"
        return self
    
    def validate_with_schema(self, schema: dict):
        """使用指定的JSON Schema来校验响应体

        Args:
            schema (dict): JSON Schema字典
        """
        if self.json_data is None:
            raise AssertionError("响应体不是有效的JSON格式, 无法进行Schema校验")
        
        try:
            validate(instance=self.json_data, schema=schema)
        except ValidationError as e:
            raise AssertionError(f"JSON Schema校验失败! \n错误信息: {e.message}\n校验路径: {list(e.path)}")
        
        return self