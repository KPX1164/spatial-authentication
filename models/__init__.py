import bcrypt

from models.user import User
from sqlalchemy import event

from .database import db


@event.listens_for(User.__table__, 'after_create')
def create_user(*args, **kwargs):
    db.session.add(User(
        email='email',
        password=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8'),
        firstname='firstname',
        lastname='lastname',
        personalised={'findmy': {'favourite': [], 'watch_later': []}, 'general': {'group_by': 'Name'}}
    ))
    db.session.commit()
