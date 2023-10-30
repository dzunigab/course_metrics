# md-apisecurity/src/app.py

from src import create_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from src.models import db


app = create_app('default')
app_context = app.app_context()
app_context.push()
# print(app.config['SQLALCHEMY_DATABASE_URI'])


# db setup
with app.app_context():
    db.create_all()
    db.session.commit()

# Cors
cors = CORS(app=app, resources={r"/security/*": {"origins": "*"}})

# JWT Auth
jwt = JWTManager(app)

# check-health-component
@app.route('/ping', methods=['GET'])
def ping():
    app_name = os.getenv('FLASK_APP_NAME')
    return {
            "message":f"pong from {app_name} app",
            "status": "success"
            }, 200