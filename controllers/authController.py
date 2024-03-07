import bcrypt
import jwt
import datetime
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy

from models.user import User

db = SQLAlchemy()

class AuthController:
    @staticmethod
    def auth():
        try:
            username = request.get_json()['username']
            password = request.get_json()['password']

            try:
                user = User.query.filter_by(username=username).first()
                if (bcrypt.checkpw(password.encode('utf-8'), bytes(user.password, 'utf-8'))):
                    user_serialize = user.serialize
                    token = jwt.encode(
                        {'user': user_serialize, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)}, 'Bearer')
                    return jsonify({'user': user_serialize, 'token': token}), 200
                raise
            except:
                return jsonify({'message': 'Username or password is incorrect'}), 401
        except KeyError:
            return jsonify({'message': 'The request body required username, password'}), 400

    @staticmethod
    def register():
        try:
            username = request.get_json()['username']
            password = request.get_json()['password']
            email = request.get_json()['email']

            # Check if the username already exists in the user table
            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                return jsonify({'message': 'Username already exists'}), 400

            # Create a new user
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'Registration successful'}), 201

        except KeyError:
            return jsonify({'message': 'The request body requires username and password'}), 400