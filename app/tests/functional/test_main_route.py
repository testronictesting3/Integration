#from app import create_app
#from flask import Flask
import pytest

def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code ==200
    assert_template_used("hello.html")

def test_return_json(test_client):
    response = test_client.post('/')
    assert response.status_code == 200
    assert test_client.json() == "Main Route"

    