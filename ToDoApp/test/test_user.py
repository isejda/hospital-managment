from fastapi import status

from .utils import *
from ..routers.users import get_db, get_current_user

app.dependency_overrides[get_db]  = override_get_db
app.dependency_overrides[get_current_user]  = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'isejda'
    assert response.json()['email'] == 'isejda@rdcom.com'
    assert response.json()['role'] == 'admin'
    assert response.json()['firstname'] == 'Isejda'
    assert response.json()['lastname'] == 'Qemali'
    assert response.json()['phoneNumber'] == '00355699149079'

def test_change_password_success(test_user):
    response = client.post("/user/change_password/", json={"password": "123", "new_password":"1234"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.post("/user/change_password/", json={"password": "WRONG", "new_password":"1234"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Please enter the correct password.'

def test_change_phone_number_success(test_user):
    response = client.put("/user/phoneNumber/123456788")
    assert response.status_code == status.HTTP_204_NO_CONTENT
