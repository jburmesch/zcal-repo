from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

from zcal import routes