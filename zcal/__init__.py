import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
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

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from zcal.auth.auth import auth
        from zcal.cal.cal import calbp
        from zcal.admin.admin import admin
        from zcal.zoom.zoom import zoom
        app.register_blueprint(auth)
        app.register_blueprint(calbp)
        app.register_blueprint(admin)
        app.register_blueprint(zoom)

    return app
