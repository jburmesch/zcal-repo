from flask_wtf import FlaskForm
from wtforms import TimeField, DateField, SubmitField
from wtforms.validators import InputRequired


class ScheduleForm(FlaskForm):
    date = DateField('Date', validators=[InputRequired()])
    time = TimeField('Time', validators=[InputRequired()])
    reserve = SubmitField('Make Reservation')
