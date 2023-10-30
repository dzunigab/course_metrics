# md-apisecurity/src/models.py

from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

# db setup
db = SQLAlchemy()

# Token
class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    token = db.Column(db.String(500))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

# Serializations
# Token
class UserTokenSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserToken
        include_relationship = True
        load_instance = True
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(40), nullable = False, unique=True)
    password = db.Column(db.String(30), nullable = False)
    createdAt = db.Column(db.DateTime, nullable = False, default = datetime.now)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

class GetUserByIdSchemaValidation(Schema):
    id = fields.Integer(required=True)
    
class GetUserLoginSchemaValidation(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

class UserBaseSchemaValidation(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)