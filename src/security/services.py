import hashlib
import requests
import json
import os

CORE_APIUSER = os.environ.get('CORE_APIUSER_URL') or 'http://127.0.0.1:9000/users'
class Services:
    
    def validateUserData(self, dataUser):
        payload = json.dumps({
            "email": dataUser['email'],
            "password": dataUser['password']
        })
        headers = {"Content-Type": "application/json"}
        print("Se golpea apiuser en url: {0} , enviando payload: {1}".format(CORE_APIUSER, payload))
        response = requests.post(CORE_APIUSER + "/validate", headers=headers, data=payload)
        print("Respuesta de api: {0}, http: {1}".format(response, response.status_code))
        if response.status_code == 200:
            return json.dumps(response.json())
        return None
    
    def salifyHash(self, profile, salt):
        salted_hash = hashlib.sha512((str(profile) + str(salt)).encode()).hexdigest()
        return salted_hash