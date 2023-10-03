from flask import Flask
from flask_bootstrap import Bootstrap
from peewee import SqliteDatabase
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect

from app.config import config
from app.error_handlers import internal_server_error, page_not_found
from app.base_model import database_proxy
from app.main.models import User, Role, Profile


def create_app(config_name='default'):
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config.from_object(config[config_name])

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    if config_name == 'testing':
        db = SqliteDatabase(':memory:', pragmas={'foreign_keys': 1})
    else:
        db = SqliteDatabase(app.config['DB_NAME'], pragmas={'foreign_keys': 1})

    database_proxy.initialize(db)
    db.create_tables([Profile, Role, User])

    csrf = CSRFProtect(app)
    csrf.init_app(app)
    app.config['CSRF'] = csrf

    moment = Moment()
    moment.init_app(app)

    Bootstrap(app)

    from app.main import main

    app.register_blueprint(main)

    return app
