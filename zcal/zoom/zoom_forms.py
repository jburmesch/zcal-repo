from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, ValidationError, IntegerField
from wtforms.validators import InputRequired, NumberRange
from zcal.models import Teacher, Zoom


class ZoomForm(FlaskForm):
    authorize = SubmitField('Add Account', validators=[InputRequired()])


class ZoomlessTeachers(FlaskForm):
    zm_id = IntegerField(validators=[InputRequired(), NumberRange(min=1)])
    teachers = SelectField('Select Teacher', coerce=int,
                           validators=[InputRequired()])
    submit = SubmitField('Set Teacher')

    def validate_teacher(self, teachers):
        tch = Teacher.query.filter_by(id=teachers.data).first()
        if tch not in Teacher.query.filter_by(zoom=None).all():
            raise ValidationError(
                'That teacher either doesn\'t exist, '
                + 'or already has a zoom account.'
            )

    def validate_zoom(self, zm_id):
        z = Zoom.query.filter_by(id=zm_id.data).first()
        if not z or z.teacher:
            raise ValidationError(
                'That zoom account either doesn\'t exist, '
                + 'or is already assigned to a teacher.'
            )