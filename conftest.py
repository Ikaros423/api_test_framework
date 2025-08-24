import pytest
import sys
from .config.settings import Settings

@pytest.fixture(scope="session")
def global_setup():
    from common.base_path import BASE_PATH
    sys.path.append(BASE_PATH)
    
@pytest.fixture(scope="session")
def settings():
    settings_instance = Settings()
    yield settings_instance