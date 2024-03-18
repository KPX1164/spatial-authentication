from .database import db
import json

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    personalised = db.Column(db.Text)  # Store as JSON

    def __init__(self, email, password, firstname=None, lastname=None, personalised=None):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.personalised = json.dumps(personalised) if personalised is not None else '{}'

    @property
    def personalised_as_dict(self):
        return json.loads(self.personalised)

    @personalised_as_dict.setter
    def personalised_as_dict(self, value):
        self.personalised = json.dumps(value)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'personalised': self.personalised_as_dict
        }
