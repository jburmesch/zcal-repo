import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(test_config=None):
    # create app
    app = Flask(__name__, instance_relative_config=True)
    # Secret generation:
    # import secrets
    # secrets.token_hex(16)
    # exit()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        db.init_app(app)
    else:
        # load the test config if testing
        app.config.from_pyfile('../testing/testconfig.py', silent=True)
        db.init_app(app)
        init_db(app)

    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():

        from zcal.auth.auth import auth
        from zcal.cal.cal import calbp
        from zcal.admin.admin import admin
        from zcal.zoom.zoom import zoom
        from zcal.day.day import day
        from zcal.users.users import users
        from zcal.meeting.meeting import meeting

        app.register_blueprint(auth)
        app.register_blueprint(calbp)
        app.register_blueprint(admin)
        app.register_blueprint(zoom)
        app.register_blueprint(day)
        app.register_blueprint(users)
        app.register_blueprint(meeting)

    return app


# BE CAREFUL WITH THIS (Should just be used for testing - DROPS ALL DB TABLES)
def init_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
