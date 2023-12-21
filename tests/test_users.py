from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
import pytest


client = TestClient(app=app)

creds = {
    "username" : "jenna@doe.com",
    "password": "password",
}

access_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE3MDMxNTQ1NTV9.M7dNYSH5OojoBHwoeQqPzYL4nSvEKz96MOb-jkTXATY"


headers =  {
    'Authorization': 'Bearer ' + access_token
}

new_todo = {
    "title" : "Todo from tests",
    "content": "content from test"
}

new = {
    "email" : "johnathan@doe.com",
    "password": "password",
}

def test_todos():
    responce = client.get("/todos")
    assert responce.status_code == 200


def test_create_user():
    responce = client.post("/auth/signup", json=new)
    # with pytest.raises(HTTPException):
    assert responce.status_code == 409


def test_login():
    responce = client.post("/auth/login", data=creds )
    assert responce.status_code == 200

def test_create_todo():
    responce = client.post("/todos", headers=headers, json=new_todo )
    assert responce.status_code == 201