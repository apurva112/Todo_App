from flask_restful import Resource, reqparse
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
from resources.decorator import token_required


class UserDetails(Resource):

    @token_required
    def get(self, p_id):
        user = Users.query.filter_by(public_id=p_id).first()

        if not user:
            return jsonify({'status': 'No user found'})

        output = [{
            'public_id': user.public_id,
            'name': user.name,
            'email': user.email
        }]

        return jsonify({'user': output})

    def post(self):

        auth = request.form

        if not auth or not auth.get('email') or not auth.get('password'):
            return make_response(
                jsonify({'status': 'Could not verify'}),
                401,
                {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
            )

        user = Users.query \
            .filter_by(email=auth.get('email')) \
            .first()

        if not user:
            return make_response(
                jsonify({'status': 'Could not verify'}),
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            )

        if check_password_hash(user.password, auth.get('password')):
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, 'secret key')

            return make_response(jsonify({'token': token}), 201)

        return make_response(
            jsonify({'status': 'Could not verify'}),
            403,
            {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
        )


class UserRegister(Resource):

    def post(self):

        # parser = reqparse.RequestParser()
        # parser.add_argument('name', type=str, required=True,
        #                     help="Username can not be left blank")
        # parser.add_argument('email', type=str, required=True,
        #                     help="Email can not be left blank")
        # parser.add_argument('password', type=str, required=True,
        #                     help="Password can not be left blank")
        # data = UserRegister.parser.parse_args()
        data = request.form

        name, email = data.get('name'), data.get('email')
        password = data.get('password')

        user = Users.query \
            .filter_by(email=email) \
            .first()
        if not user:
            user = Users(
                public_id=str(uuid.uuid4()),
                name=name,
                email=email,
                password=generate_password_hash(password)
            )
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(minutes=30),
            }, 'secret key', "HS256")

            db.session.add(user)
            # db.session.commit()
            try:
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close()

            return make_response(jsonify({'token': token}), 201)

        else:
            return make_response(jsonify({'status': 'User already exists. Please Log in.'}), 202)


class UsersDetails(Resource):

    @token_required
    def get(self, curr_user):

        output = []
        for user in users:
            output.append({
                'public_id': user.public_id,
                'name': user.name,
                'email': user.email
            })

        return make_response(jsonify({'users': output}), 401)
