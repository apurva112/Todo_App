from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from db import db
from models.user import Users
from models.tasks import Tasks
from functools import wraps
from flask_restful import Resource, Api
from resources.decorator import token_required
from resources.user import UserRegister, UserDetails, UsersDetails
from resources.tasks import Todos

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Cab2001@localhost/sql_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
api = Api(app)
# db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


api.add_resource(UserRegister, '/register')
api.add_resource(UsersDetails, '/users')
api.add_resource(UserDetails, '/user')
# api.add_resource(UserDetails, '/user/<string:p_id>')
api.add_resource(Todos, '/tasks')


# user = User(id = 1, public_id= "1234", name = 'Test Name',email = 'Test Email',password = 'Password')
# db.session.add(user)
#
# try:
#     db.session.commit()
# except:
#     db.session.rollback()
# finally:
#     db.session.close()


if __name__ == '__main__':
    app.run()
