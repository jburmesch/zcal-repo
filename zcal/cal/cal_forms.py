from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, Email


class TeacherSchedule(FlaskForm):
    date = DateField(validators=[InputRequired()])
    slots = StringField()


class ZoomForm(FlaskForm):
    account = StringField(
        "Account Email",
        validators=[InputRequired(),
                    Length(max=120),
                    Email()]
    )
    authorize = SubmitField('Authorize Account')
