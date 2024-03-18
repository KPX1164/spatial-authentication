import json
import bcrypt
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy_utils.functions import database_exists, create_database

from controllers.authController import AuthController
from models import User
from models.database import db
from routes.auth import AuthBlueprint

app = Flask(__name__)
# CORS(app, resources={r'/*': {'origins': '*'}})
CORS(app)

app.config.from_object('config')

if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])
    print('Creating a database')

db.init_app(app)
with app.app_context():
    db.create_all()

class FlaskApp:
    app.register_blueprint(AuthBlueprint.auth_bp)

@app.route('/sign-in', methods=['POST'])
def AuthLogin():
    return AuthController.auth()

@app.route('/auth/sign-up', methods=['POST'])
def register():
    try:
        email = request.get_json()['email']
        password = request.get_json()['password']
        firstname = request.get_json()['firstname']
        lastname = request.get_json()['lastname']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({'message': 'Email already exists'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        personalised = {'favourite': [], 'general': {'group_by': 'Name'}}
        new_user = User(email=email, password=hashed_password, firstname=firstname, lastname=lastname, personalised=personalised)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registration successful'}), 201

    except KeyError:
        return jsonify({'message': 'The request body requires username and password'}), 400


@app.route('/update-group-by', methods=['PUT'])
def update_group_by():
    try:
        # Get the email and selected option from the request data
        email = request.get_json()['email']
        selected_option = request.get_json()['selectedOption']

        # Find the user with the given email
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Parse the personalised field into a dictionary
        personalised = json.loads(user.personalised)

        # Update the group_by field in the personalised object
        personalised['general']['group_by'] = selected_option

        # Convert the personalised dictionary back into a JSON string
        user.personalised = json.dumps(personalised)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Group by option updated successfully'}), 200

    except KeyError:
        return jsonify({'message': 'The request body requires email and selectedOption'}), 400


@app.route('/update-findmy', methods=['PUT'])
def update_findmy(folder):
    try:
        # Get the email and value to append from the request data
        email = request.get_json()['email']
        value_to_append = request.get_json()['value']

        # Find the user with the given email
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Parse the personalised field into a dictionary
        personalised = json.loads(user.personalised)

        # Ensure the folder is valid
        if folder not in personalised['findmy']:
            return jsonify({'message': f'Invalid folder: {folder}'}), 400

        # Append the value to the specified folder
        personalised['findmy'][folder].append(value_to_append)

        # Convert the personalised dictionary back into a JSON string
        user.personalised = json.dumps(personalised)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': f'Item added to {folder} successfully'}), 200

    except KeyError:
        return jsonify({'message': 'The request body requires email and value'}), 400

@app.route('/add-to-favorites/<int:user_id>/<int:spatial_id>', methods=['POST'])
def add_to_favorites(user_id, spatial_id):
    try:
        # Get the user by user_id
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Parse the personalised field into a dictionary
        personalised = json.loads(user.personalised)

        # Extract the findmy data
        findmy_data = personalised.get('findmy', {})

        # Add spatialID to favorites list
        findmy_data.setdefault('favourite', []).append(spatial_id)

        # Update the personalised field in the user object
        user.personalised = json.dumps(personalised)

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': f'SpatialID {spatial_id} added to favorites successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/findmy/<int:user_id>', methods=['GET'])
def get_findmy_by_user_id(user_id):
    try:
        # Find the user by ID
        user = User.query.get(user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Parse the personalised field into a dictionary
        personalised = json.loads(user.personalised)

        # Extract the findmy data
        findmy_data = personalised.get('findmy', {})

        return jsonify({'findmy': findmy_data}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Test route is working"})

if __name__ == '__main__':
    app.run(debug=False)
