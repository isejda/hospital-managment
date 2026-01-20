from fastapi import HTTPException

from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from jose import jwt
from datetime import timedelta
import pytest

app.dependency_overrides[get_db]  = override_get_db

def test_authenticate_user(test_user):
    db = TestSessionLocal()
    authenticated_user = authenticate_user(test_user.username, '123', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

def test_non_existing_user(test_user):
    db = TestSessionLocal()
    non_existing_user = authenticate_user('wrongUsername', '123', db)
    assert non_existing_user is False

def test_wrong_password_user(test_user):
    db = TestSessionLocal()
    wrong_password_user = authenticate_user(test_user.username, 'wrongPassword', db)
    assert wrong_password_user is False

def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username=username, user_id=user_id, role=role, expires_delta=expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature': False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode={'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'testuser', 'id': 1, 'role': 'admin'}

@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    encode={'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as e:
        await get_current_user(token=token)

    assert e.value.status_code == 401
    assert e.value.detail == 'COULD NOT VALIDATE USER'
