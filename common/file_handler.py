import json
import yaml
import os
from .base_path import BASE_PATH

def load_json_schema(file_path: str) -> dict:
    """加载schemas目录下的json文件

    Args:
        file_path (str): 相对于schemas目录的文件路径

    Returns:
        dict: jsonschema需要的字典类型
    """
    full_path = os.path.join(BASE_PATH, 'schemas', file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_yaml_data(file_path: str) -> dict:
    """加载data目录下的yaml文件

    Args:
        file_path (str): 相对于data目录的文件路径

    Returns:
        dict: 字典
    """
    full_path = os.path.join(BASE_PATH, 'data', file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)