import pytest
import sys

@pytest.fixture(scope="session")
def global_setup():
    from common.base_path import BASE_PATH
    sys.path.append(BASE_PATH)
    yield