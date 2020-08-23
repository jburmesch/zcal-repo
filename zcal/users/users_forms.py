from flask_wtf import FlaskForm
from zcal import bcrypt
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField, IntegerField
)
from zcal.models import User
from wtforms.validators import (
    InputRequired, Length, Email, ValidationError, EqualTo
)


class NameForm(FlaskForm):
    name = StringField(
        validators=[InputRequired(), Length(max=120)]
    )
    name_type = StringField(
        validators=[InputRequired()]
    )
    submit = SubmitField()

    def validate_name_type(self, name_type):
        if name_type.data != 'First' and name_type.data != 'Last':
            raise ValidationError('NameType Error.')


class EmailForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Email(), Length(max=120)]
    )
    confirm_email = StringField(
        validators=[InputRequired(), EqualTo('email'), Length(max=120)]
    )
    submit = SubmitField()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email address has already been registered.'
            )


class PasswordForm(FlaskForm):
    user_field = IntegerField(validators=[InputRequired()])
    password = PasswordField(
        validators=[InputRequired()]
    )
    new_password = PasswordField(
        validators=[InputRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        validators=[InputRequired(), EqualTo('new_password')]
    )
    submit = SubmitField()

    def validate_password(self, password):
        u = User.query.filter(User.id == self.user_field.data).one()
        if not u or not bcrypt.check_password_hash(
            u.password,
            password.data
        ):
            raise ValidationError('Invalid Password')


class AdminForm(FlaskForm):
    code = StringField(
        validators=[Length(max=10)]
    )
    utype = SelectField(choices=[
        ('Change', 'Change'),
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Admin', 'Admin')
    ])
    submit = SubmitField()

    # def validate_code(self, code):
    #     c = Course.query.filter(Course.code == code.data).one()
    #     if c is None:
    #         raise ValidationError('Course Code Not Found')
