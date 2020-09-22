from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.fields.html5 import TimeField, IntegerField
from wtforms.validators import (
    InputRequired, Length, Email, ValidationError, NumberRange, EqualTo
)
from zcal.models import User, Course


def get_courses():
    the_list = []
    courses = Course.query.all()
    for course in courses:
        if course.name != 'ADMIN':
            tup = (course.name, course.name)
            the_list.append(tup)
    return the_list


class UserForm(FlaskForm):
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
    course = SelectField(
        'Course',
        choices=get_courses()
    )
    user_type = SelectField(
        'User Type',
        choices=[
            ('Student', 'Student'),
            ('Teacher', 'Teacher'),
            ('Admin', 'Admin')
        ], validators=[InputRequired()]
    )
    submit = SubmitField('Create')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email address has already been registered.'
            )


class CourseForm(FlaskForm):
    name = StringField(
        'Course Name',
        validators=[InputRequired(), Length(max=120)]
    )
    code = StringField(
        'Course Code',
        validators=[InputRequired(), Length(max=120)]
    )
    submit = SubmitField('Register')

    def validate_name(self, name):
        course = Course.query.filter_by(name=name.data).first()
        if course:
            raise ValidationError(
                'A course with this name already exists.'
            )

    def validate_code(self, code):
        course = Course.query.filter_by(code=code.data).first()
        if course:
            raise ValidationError(
                'A course with this code already exists.'
            )


class TimeslotForm(FlaskForm):
    start = TimeField('Start time', validators=[InputRequired()])
    duration = IntegerField(
        'Duration',
        validators=[
            InputRequired(),
            NumberRange(
                min=10,
                max=120,
                message='Meetings must be between 10 and 120 minutes.'
            )
        ]
    )
    add = SubmitField('Add')


class RemoveForm(FlaskForm):
    rem_type = StringField()
    rem_id = IntegerField(validators=[InputRequired(), NumberRange(min=1)])
    remove = SubmitField('Remove')


class ManageForm(FlaskForm):
    mg_id = IntegerField(validators=[InputRequired(), NumberRange(min=1)])
    form_id = StringField()
    manage = SubmitField('Manage')
