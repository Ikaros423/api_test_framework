from ..common.read_config import get_base_url
import httpx
import pytest

def test_somke():
    client = httpx.Client()
    url = get_base_url()
    response = client.get(url=url)
    assert response.status_code == 200
