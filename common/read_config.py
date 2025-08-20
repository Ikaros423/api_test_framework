from .base_path import BASE_PATH
import yaml

def get_base_url():
    config_path = BASE_PATH + r'\config\config.yaml'
    with open(config_path,"r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config['base_url']

if __name__ == '__main__':
    print(get_base_url())