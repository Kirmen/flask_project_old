from peewee import CharField, DateTimeField, TextField, ForeignKeyField
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from app.base_model import BaseModel


class Role(BaseModel):
    name = CharField(max_length=100, unique=True, index=True)


class Profile(BaseModel):
    avatar = CharField()
    info = TextField(null=True)


class User(BaseModel):
    username = CharField(max_length=100, index=True)
    email = CharField(max_length=200, unique=True, index=True)
    __password_hash = CharField(max_length=128)
    last_visit = DateTimeField(default=datetime.datetime.now)
    role = ForeignKeyField(Role, backref='users')
    profile = ForeignKeyField(Profile)

    @property
    def password(self):
        raise AttributeError('password is not a valid attribute')

    @password.setter
    def password(self, password):
        self.__password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.__password_hash, password)

