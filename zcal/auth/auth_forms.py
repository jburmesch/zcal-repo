from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import (
    InputRequired, Length, Email, ValidationError, EqualTo
)
from zcal.models import User, Course


class RegistrationForm(FlaskForm):
    code = StringField(
        'Course Code',
        validators=[InputRequired(), Length(max=10)]
    )
    first = StringField(
        'First Name',
        validators=[InputRequired(), Length(max=120)]
    )
    last = StringField(
        'Last Name',
        validators=[InputRequired(), Length(max=120)]
    )
    email = StringField(
        'Email Address',
        validators=[InputRequired(), Email(), Length(max=120)]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[InputRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email address has already been registered.'
            )

    def validate_code(self, code):
        course = Course.query.filter_by(code=code.data).first()
        # make it so admin code only works for first user
        # to log in with admin course
        # otherwise, make sure course exists
        if not course:
            raise ValidationError(
                'Course code not found.'
            )
        elif course.id == 1:
            user = User.query.all()
            if user:
                raise ValidationError(
                    'Course code not found.'
                )


class LoginForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[InputRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired()]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
