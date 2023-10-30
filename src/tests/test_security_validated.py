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

class TestValidateToken(unittest.TestCase):
    
    @patch.object(Services, "validateUserData")
    def setUp(self, mock_call_user):
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
        mock_call_user.return_value = '{"id": 123, "profile": "CANDIDATO"}' 
        usuario = {
            "email": self.userFake['email'],
            "password":  self.userFake['password']
        }
        endpoint_login = "/security/login"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}"}

        solicitud = self.client.post(endpoint_login, data=json.dumps(usuario), headers=headers)
        response = json.loads(solicitud.get_data())
        
        self.token = response["token"]
        
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        
    def test_validate_token_success(self):
        endpoint_login = "/security/candidate/auth"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud = self.client.get(endpoint_login, headers=headers)
        response = json.loads(solicitud.get_data())        

        self.assertEqual(solicitud.status_code, 200)
        self.assertEqual(response['status'], "success")
        
    def test_validate_without_token(self):
        endpoint_login = "/security/candidate/auth"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}"}

        solicitud = self.client.get(endpoint_login, headers=headers) 
        self.assertEqual(solicitud.status_code, 422)
        
    def test_validate_invalid_token(self):
        invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NDkxODMwOCwianRpIjoiYjg3YmZhNjAtODU4Yi00MTA5LTg4ODAtOTM4YjI5MGUyMDJjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjk0OTE4MzA4LCJleHAiOjE2OTQ5MjE5MDh9.KCru7JS-e1tiu7UGp62tmMGfBlMqFFJlZmPDirHY4io"
        endpoint_login = "/security/candidate/auth"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(invalid_token)}

        solicitud = self.client.get(endpoint_login, headers=headers)      

        self.assertEqual(solicitud.status_code, 422)
        
    def test_validate_modified_token(self):
        endpoint_login = "/security/candidate/auth"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}{}".format(self.token, self.data_factory.word())}
        

        solicitud = self.client.get(endpoint_login, headers=headers)       

        self.assertEqual(solicitud.status_code, 422)
        
    def test_validate_auth_token_candidate_success(self):
        endpoint_login = "/security/candidate/auth"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        

        solicitud = self.client.get(endpoint_login, headers=headers)       

        self.assertEqual(solicitud.status_code, 200)
        
    def test_validate_auth_token_company_fail(self):
        endpoint_login = "/security/company/auth"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        

        solicitud = self.client.get(endpoint_login, headers=headers)       

        self.assertEqual(solicitud.status_code, 403)
        
    def test_validate_auth_token_abcjobs_fail(self):
        endpoint_login = "/security/abcjobs/auth"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        

        solicitud = self.client.get(endpoint_login, headers=headers)       

        self.assertEqual(solicitud.status_code, 403)
