# md-apisecurity/src/tests/test_basics.py
import json
import unittest
from unittest.mock import patch
import sys
sys.path.append("..")
from flask_jwt_extended import JWTManager
from faker import Faker
from faker.generator import random
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
        
    @patch.object(Services, "validateUserData")
    def test_validate_login_correct(self, mock_call_user):
        
        usuario = {
            "email": self.userFake['email'],
            "password":  self.userFake['password']
        }
        mock_call_user.return_value = '{"id": 123,"profile": "candidate"}'

        endpoint_login = "/security/login"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}"}

        solicitud = self.client.post(endpoint_login, data=json.dumps(usuario), headers=headers)
        response = json.loads(solicitud.get_data())

        self.assertEqual(solicitud.status_code, 200)
        
    
    def test_validate_login_error_format(self):
        
        usuario = {
            "correo": self.userFake['email'],
            "password":  self.userFake['password']
        }

        endpoint_login = "/security/login"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}"}

        solicitud = self.client.post(endpoint_login, data=json.dumps(usuario), headers=headers)
        response = json.loads(solicitud.get_data())

        self.assertEqual(solicitud.status_code, 422)
        self.assertEqual(response['status'], "error")
        
    @patch.object(Services, "validateUserData")    
    def test_validate_login_user_not_found(self, mock_call_user):
        mock_call_user.return_value = None
        usuario = {
            "email": self.data_factory.email(),
            "password":  self.data_factory.pystr()
        }

        endpoint_login = "/security/login"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}"}

        solicitud = self.client.post(endpoint_login, data=json.dumps(usuario), headers=headers)
        response = json.loads(solicitud.get_data())

        self.assertEqual(solicitud.status_code, 404)
        self.assertEqual(response['status'], "error")
