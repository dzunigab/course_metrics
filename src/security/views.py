# md-apisecurity/src/security/views.py

from flask_restful import Resource, Api
from flask import Blueprint, request
import json
from sqlalchemy import select
import requests
from ..models import db, UserTokenSchema, GetUserLoginSchemaValidation, User, UserToken
import hashlib, jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from .profiles import ValidateProfile
from .services import Services
from ..config import Config
from flask_cors import cross_origin

user_schema = UserTokenSchema()

# blueprint
security_api = Blueprint("security_api", __name__, url_prefix="/security/")
api = Api(security_api)

# /security/login
class UsersLoginResource(Resource):
    def __init__(self):
        self.services = Services()

    @cross_origin()
    def post(self):
        data = request.json
        schema = GetUserLoginSchemaValidation()
        try:
            schema.load(data)
        except ValidationError as err:
            return {"message": "Error en el formato de solicitud", "status": "error"}, 422
        user = self.services.validateUserData(data)
        if user is None:
            return {"message": "Revise los datos e intente nuevamente", "status": "error"}, 404
        else:
            user = json.loads(user)
            token = UserToken.query.filter(UserToken.user_id == user["id"]).one_or_none()
            if token != None:
                db.session.delete(token)
                db.session.commit()
            salted_hash = self.services.salifyHash(user["profile"], user["id"])
            additional_claims = {"profile": salted_hash}
            
            token_de_acceso = create_access_token(identity=user["id"], additional_claims = additional_claims)
            new_userToken = UserToken(user_id = user["id"], token = token_de_acceso)
            db.session.add(new_userToken)
            db.session.commit()
            return {
                "message": "Inicio de sesión exitoso",
                "token": token_de_acceso, 
                "status": "success",
                "user_id": user["id"], 
                **user
                }
# /security/candidate/auth
class AuthCandidateResource(Resource):
    @ValidateProfile.candidato_required()
    def get(self):
        return {"message": "Token validado", "status": "success"}, 200

# /security/company/auth
class AuthCompanyResource(Resource):
    @ValidateProfile.empresa_required()
    def get(self):
        return {"message": "Token validado", "status": "success"}, 200

# /security/abcjobs/auth
class AuthAbcjobsResource(Resource):
    @ValidateProfile.abcjobs_required()
    def get(self):
        return {"message": "Token validado", "status": "success"}, 200

# /security/ping
class PingUserResource(Resource):

    def get(self):
        return {"message": "pong", "status": "success"}

# /person    

# add resources
api.add_resource(UsersLoginResource, '/login')
api.add_resource(AuthCandidateResource, '/candidate/auth')
api.add_resource(AuthCompanyResource, '/company/auth')
api.add_resource(AuthAbcjobsResource, '/abcjobs/auth')
api.add_resource(PingUserResource, '/ping')