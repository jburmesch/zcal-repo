from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
                    BooleanField, TimeField, DateField
from wtforms.validators import DataRequired, Length, Email, \
                               EqualTo, ValidationError
from zcal.models import User, Course


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
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email address has already been registered.'
            )


class CourseForm(FlaskForm):
    name = StringField(
        'Course Name',
        validators=[DataRequired(), Length(max=120)]
    )
    code = StringField(
        'Course Code',
        validators=[DataRequired(), Length(max=120)]
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


class RegistrationForm(FlaskForm):
    code = StringField(
        'Course Code',
        validators=[DataRequired(), Length(max=10)]
    )
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

    def validate_code(self, code):
        course = Course.query.filter_by(code=code.data).first()
        # make it so admin code only works for first user
        # to log in with admin course
        if course.id == 1:
            user = User.query.all()
            if user:
                raise ValidationError(
                    'Course code not found.'
                )
        # otherwise, make sure course exists
        if not course:
            raise ValidationError(
                'Course code not found.'
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
