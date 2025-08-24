import yaml
from ..common.base_path import BASE_PATH

class Settings():
    def __init__(self):
        config_path = BASE_PATH + r'\config\config.yaml'
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
            
    def get(self, key: str):
        try:
            return self.config.get(key)
        except Exception as e:
            raise