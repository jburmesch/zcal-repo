from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# create app
app = Flask(__name__)
# set config variables -> switch to env variables in future
app.config['SECRET_KEY'] = 'dev'

# Secret generation:
# import secrets
# secrets.token_hex(16)
# exit()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zcal.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from zcal.routes import auth, cal  # noqa
