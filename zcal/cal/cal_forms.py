from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired


class TeacherSchedule(FlaskForm):
    date = DateField(validators=[InputRequired()])
    slots = StringField("", validators=[InputRequired()])
    submit = SubmitField()
