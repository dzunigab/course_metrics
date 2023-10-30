# md-apisecurity/src/__init__.py

from flask import Flask
from src import config
from flask_sqlalchemy import SQLAlchemy
from src.models import db
from dotenv import load_dotenv
import os
from src.security.views import security_api


# app constructor
def create_app(config_name=None):
    app = Flask(__name__)

    # set config
    config_name = os.getenv('FLASK_ENV', 'development')

    # load .env file
    if config_name == 'development':
        env_file = '.env'
    elif config_name == 'testing':
        env_file = '.env.test'
    elif config_name == 'production':
        env_file = '.env.prod'
    else:
        env_file = '.env'

    load_dotenv(env_file)

    # set configuration
    if config_name == 'development':
        app.config.from_object(config.DevelopmentConfig)
    elif config_name == 'testing':
        app.config.from_object(config.TestingConfig)
    elif config_name == 'production':
        app.config.from_object(config.ProductionConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

    # set up database    
    db.init_app(app)

    # register blueprints
    app.register_blueprint(security_api)

    return app