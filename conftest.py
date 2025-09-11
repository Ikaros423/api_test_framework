import pytest
import asyncio
import sys
import httpx
from .config.settings import Settings

@pytest.fixture(scope="session")
def global_setup():
    from common.base_path import BASE_PATH
    sys.path.append(BASE_PATH)
    
@pytest.fixture(scope="session")
def settings():
    settings_instance = Settings()
    yield settings_instance

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        try:
            asyncio.set_event_loop(None)
        except Exception:
            pass
        loop.close()

@pytest.fixture(scope="session")
def httpx_client(event_loop, base_url):
    # 在 session 的 event_loop 上运行 AsyncClient 的 __aenter__/aclose 操作
    client = httpx.AsyncClient(base_url=base_url)
    event_loop.run_until_complete(client.__aenter__())
    try:
        yield client
    finally:
        event_loop.run_until_complete(client.aclose())