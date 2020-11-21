
from app_folder import create_app
import pytest
app=create_app()

def test_login():
      with app.test_client() as client:
            response = client.post('/login', data=dict(
            ), follow_redirects=True)
            
            assert b'<h1 class="sign-in"> Sign in</h1>' in response.data

def test_logout():
         with app.test_client() as client:
            response = client.post('/logout', data=dict(
            )
            , follow_redirects=True)
            assert b'Welcome to Appoinment schedule system!' in response.data