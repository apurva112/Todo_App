from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, date, timedelta
from db import db
from models.user import Users
from models.tasks import Task
from functools import wraps
from flask_restful import Resource, Api
from resources.decorator import token_required
from resources.user import UserRegister, UserDetails, UsersDetails
from resources.tasks import TodoClass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hpfzdzpolnvfbe:97575946dfc02283cdcc3dbb42eef04ff1d106093b1f711152601b70190d3f7a@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/d7gjioccn9kn50'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
api = Api(app)
# db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=["GET"])
def hello_world():  # put application's code here
    # users = Users.query.all()
    date_today = date.today()
    task = Task(title='Task 3', description="Complete Task 3", user_id="972ea6f9-8957-4b35-a05e-27cb33b22dcd",
                completed=False, initial_date=date_today,
                last_date=date_today + timedelta(days=3), user_order=1,
                last_update=date_today, deleted=None)
    db.session.add(task)
    db.session.commit()
    # try:
    #     db.session.commit()
    # except:
    #     db.session.rollback()
    # finally:
    #     db.session.close()
    return make_response(jsonify({"status": "Done"}))




api.add_resource(UserRegister, '/register')
api.add_resource(UsersDetails, '/users')
api.add_resource(UserDetails, '/user')
# api.add_resource(UserDetails, '/user/<string:p_id>')
api.add_resource(TodoClass, '/tasks')

# user = User(id = 1, public_id= "1234", name = 'Test Name',email = 'Test Email',password = 'Password')
# db.session.add(user)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
