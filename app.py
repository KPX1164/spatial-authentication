import json

import bcrypt
from flask import Flask, request, jsonify
from flask_cors import CORS
# from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils.functions import database_exists, create_database

# from controllers import authController
from controllers.authController import AuthController
# from controllers.compareController import CompareController
from models import User
from models.database import db
from routes.auth import AuthBlueprint

# from routes.compare_bp import CompareBlueprint

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config.from_object('config')

if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])
    print('Creating a database')

db.init_app(app)
with app.app_context():
    db.create_all()


class FlaskApp:
    app.register_blueprint(AuthBlueprint.auth_bp)
    # app.register_blueprint(CompareBlueprint.compare_bp)


@app.route('/login', methods=['POST'])
def AuthLogin():
    return AuthController.auth()


@app.route('/auth/register', methods=['POST'])
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


@app.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Test route is working"})


# @app.route('/summary', method=['POST'])
# def compare():
#     return CompareController.addCost()

if __name__ == '__main__':
    app.run(debug=False)
