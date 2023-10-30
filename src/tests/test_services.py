# md-apisecurity/src/tests/test_basics.py
import json
import unittest
from unittest.mock import patch
import sys
sys.path.append("..")
from flask_jwt_extended import JWTManager
from faker import Faker
from src import create_app, db
from src.security.services import Services

class TestGenerateToken(unittest.TestCase):
    
    def setUp(self):
        self.data_factory = Faker()
        self.app = create_app('testing')
        jwt = JWTManager(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.userFake = {
            "name": self.data_factory.name(),
            "email":self.data_factory.email(),
            "password": self.data_factory.pystr()
        }
        
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    @patch("requests.post")
    def test_validate_user_data(self, mock_call_user):
        apiUser = "http://test.com"
        usuario = {
            "email": self.userFake['email'],
            "password":  self.userFake['password']
        }
        mock_call_user.return_value.status_code = 200
        mock_call_user.return_value.json.return_value = {
                "id": 123,
                "profile": "candidate"
            }
        
        response_method = json.loads(Services().validateUserData(usuario))

        self.assertEqual(response_method["id"], 123)
        
    @patch("requests.post")
    def test_validate_user_data_error(self, mock_call_user):
        apiUser = "http://test.com"
        usuario = {
            "email": self.userFake['email'],
            "password":  self.userFake['password']
        }
        mock_call_user.return_value.status_code = 404
        mock_call_user.return_value.json.return_value = {
                "id": 123,
                "profile": "candidate"
            }
        
        response_method = Services().validateUserData(usuario)

        self.assertEqual(response_method, None)
        
    
   
