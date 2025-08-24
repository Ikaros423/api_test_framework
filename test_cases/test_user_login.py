from ..apis.user_api import UserAPI
import pytest

def test_login_success(user_api):
    accounts = '123456'
    pwd = '10446949'
    type = 'username'
    response = user_api.login(accounts, pwd, type)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['msg'] == '登录成功'
    assert response_data['code'] == 0

def test_login_error_password(user_api):
    accounts = '123456'
    pwd = '1044694'
    type = 'username'
    response = user_api.login(accounts, pwd, type)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['msg'] == '密码错误'
    assert response_data['code'] == -4

def test_login_error_account(user_api):
    accounts = '12345'
    pwd = '1044694'
    type = 'username'
    response = user_api.login(accounts, pwd, type)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['msg'] == '帐号不存在'
    assert response_data['code'] == -3