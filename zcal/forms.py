from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
                    BooleanField, TimeField, DateField
from wtforms.validators import DataRequired, Length, Email, \
                               EqualTo, ValidationError
from zcal.models import User


class TeacherForm(FlaskForm):
    first = StringField(
        'First Name',
        validators=[DataRequired(), Length(max=120)]
    )
    last = StringField(
        'Last Name',
        validators=[DataRequired(), Length(max=120)]
    )
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    zoom = StringField(
        'Zoom Account',
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email address has already been registered.'
            )


class RegistrationForm(FlaskForm):
    first = StringField(
        'First Name',
        validators=[DataRequired(), Length(max=120)]
    )
    last = StringField(
        'Last Name',
        validators=[DataRequired(), Length(max=120)]
    )
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email address has already been registered.'
            )


class LoginForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class ScheduleForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    reserve = SubmitField('Make Reservation')
