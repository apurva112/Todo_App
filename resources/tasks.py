from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from db import db
from models.user import Users
from models.tasks import Task
from functools import wraps
from resources.decorator import token_required


def getUserOrder(userId):
    tasks = Task.query.filter_by(user_id=userId)
    order = 0
    for i in tasks:
        order += 1
    return order


class TodoClass(Resource):

    @token_required
    def get(self, curr_user):
        all_tasks = Task.query.filter_by(user_id=curr_user['public_id'])
        if all_tasks is None:
            return make_response(jsonify({'status': 'No Task Found'}), 200)
        else:
            result = {}
            for i in all_tasks:
                if not i.deleted:
                    result[i.id] = {"title": i.title, "description": i.description, "user_id": i.user_id,
                                    "completed": i.completed, "last_date": i.last_date, "last_update": i.last_update,
                                    "user_order": i.user_order}
        return make_response(jsonify(result), 200)

    @token_required
    def post(self, curr_user):
        content = request.headers.get('Content-Type')
        if content == 'application/json':
            json = request.get_json()
            if json['user_id'] != curr_user['public_id']:
                return make_response(jsonify({'error': 'Access Not Allowed'}), 401)
            user_order = getUserOrder(curr_user['public_id'])
            date_today = datetime.date.today()
            task = Task(title=json['title'], description=json['description'], user_id=json['user_id'],
                        completed=json['completed'], initial_date=date_today,
                        last_date=date_today + datetime.timedelta(days=json["number_of_days"]), user_order=user_order,
                        last_update=date_today, deleted=None)
            db.session.add(task)
            try:
                db.session.commit()
                return make_response(jsonify({"status": "Successfully Added to Database"}), 200)
            except:
                db.session.rollback()
                return make_response(jsonify({"status": "Error in adding task to Database"}), 400)
            finally:
                db.session.close()
                return make_response(jsonify({"status": "Request Recieved"}), 200)
        else:
            return make_response(jsonify({"status": "Content Type not Supported"}), 200)

    @token_required
    def patch(self, curr_user):
        content = request.headers.get('Content-Type')
        if content == 'application/json':
            json = request.get_json()
            if json['user_id'] != curr_user['public_id']:
                return make_response(jsonify({'error': 'Access Not Allowed'}), 401)
            user = json['user_id']
            taskid = json['id']
            temp = Task.query.filter_by(user_id=user).filter_by(id=taskid).first()
            temp.title = json['title']
            temp.description = json['description']
            temp.completed = json['completed']
            temp.last_date = temp.initial_date + datetime.timedelta(days=json["number_of_days"])
            temp.last_update = datetime.date.today()
            try:
                db.session.commit()
                return make_response(jsonify({"status": "Successfully Modified in Database"}), 200)
            except:
                db.session.rollback()
                return make_response(jsonify({"status": "Error in patching task to Database"}), 400)
            finally:
                db.session.close()
                return make_response(jsonify({"status": "Patch Request Recieved"}), 200)
        else:
            return make_response(jsonify({"status": "Content Type not Supported"}), 200)

    @token_required
    def delete(self, curr_user):
        content = request.headers.get('Content-Type')
        if content == 'application/json':
            json = request.get_json()
            if json['user_id'] != curr_user['public_id']:
                return make_response(jsonify({'error': 'Access Not Allowed'}), 401)
            user = json['user_id']
            taskid = json['id']
            temp = Task.query.filter_by(user_id=user).filter_by(id=taskid).first()
            temp.deleted = date.today()
            temp.user_order = 0
            try:
                db.session.commit()
                reorder()
                return make_response(jsonify({"status": "Successfully Deleted from Database"}), 200)
            except:
                db.session.rollback()
                return make_response(jsonify({"status": "Error in Deleting task to Database"}), 400)
            finally:
                db.session.close()
                return make_response(jsonify({"status": "Delete Request Recieved"}), 200)
        else:
            return make_response(jsonify({"status": "Content Type not Supported"}), 200)
