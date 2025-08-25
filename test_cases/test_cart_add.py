import pytest
from ..apis.cart_api import CartAPI

def test_cart_add_successfully(cart_api):
    goods_data = "W3siZ29vZHNfaWQiOjYsInN0b2NrIjoxLCJzcGVjIjpbXX1d"
    response = cart_api.add(goods_data)
    assert response.status_code == 200
    response_data = response.json()

    assert response_data['msg'] == '加入成功'
    assert response_data['code'] == 0

def test_cart_add_failed(cart_api):
    goods_data = "W3siZ29vZHNfaWQi"
    response = cart_api.add(goods_data)
    assert response.status_code == 200
    response_data = response.json()

    assert response_data['msg'] == '参数错误'
    assert response_data['code'] == -1
