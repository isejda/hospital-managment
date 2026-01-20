from fastapi import status

from .utils import *
from ..routers.todos import get_db, get_current_user

app.dependency_overrides[get_db]  = override_get_db
app.dependency_overrides[get_current_user]  = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get('/todos/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'complete': False,
        'title': 'learn the codee!',
        'description': 'Need to learn everyday',
        'id': 1,
        'priority': 5,
        'owner_id': 1,
    }]

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'complete': False,
        'title': 'learn the codee!',
        'description': 'Need to learn everyday',
        'id': 1,
        'priority': 5,
        'owner_id': 1,
    }

def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todos/todos/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}


def test_create_new_todo(test_todo):
    request_data={
        'title': 'New todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = client.post('/todos/todos', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo(test_todo):
    request_data={
        'title': 'Changed title of todo!',
        'description': 'Need to learn everyday',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todos/todos/1', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo_not_found(test_todo):
    request_data={
        'title': 'Changed title of todo!',
        'description': 'Need to learn everyday',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todos/todos/999', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}

def test_delete_todo(test_todo):
    response = client.delete('/todos/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete('/todos/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}