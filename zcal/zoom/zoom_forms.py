from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import InputRequired


class ZoomForm(FlaskForm):
    authorize = SubmitField('Add Account', validators=[InputRequired()])
