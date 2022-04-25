from flask import Flask, request, jsonify, make_response
import jwt
from models.user import Users
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'status': 'Token is missing!'}), 401)

        try:
            data = jwt.decode(token, 'secret key', algorithms=["HS256"])
            print(data)
            curr_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return make_response(jsonify({'status': 'Token is Missing'}), 401)
        return f(curr_user, *args, **kwargs)

    return decorated
