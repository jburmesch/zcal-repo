from flask import (render_template, Blueprint)
from flask_login import login_required
from zcal import db
from zcal.admin.admin_forms import RemoveForm
from zcal.models import Meeting, Student, Schedule, Teacher
import datetime


day = Blueprint('day', __name__)


@day.route('/teacher/<string:date>/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def t_meetings(date, u_id):
    date_parts = date.split("-")
    m_rem_form = RemoveForm
    s_rem_form = RemoveForm
    
    # remove timeslot when remove form is submitted.
    if s_rem_form.validate_on_submit():
        r_sched = Schedule.query.filter_by(
            id == s_rem_form.rem_id.data
        ).first()
        db.session.delete(r_sched)
        db.session.commit()

    schedules = Schedule.query.join(
        Teacher
    ).filter(
        Schedule.date == datetime.date(
            year=int(date_parts[0]),
            month=int(date_parts[1]),
            day=int(date_parts[2])
        )
    ).filter(
        Teacher.user_id == u_id
    ).all()

    meetings = Meeting.query.join(
        Schedule
    ).join(
        Teacher
    ).filter(
        Teacher.user_id == u_id
    ).filter(
        Schedule.date == datetime.date(
            year=int(date_parts[0]),
            month=int(date_parts[1]),
            day=int(date_parts[2])
        )
    ).all()

    return render_template(
        'day.html',
        teacher=True,
        date=date,
        meetings=meetings,
        schedules=schedules,
        m_rem_form=m_rem_form,
        s_rem_form=s_rem_form
    )


@day.route('/student/<string:date>/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def s_meetings(date, u_id):
    date_parts = date.split("-")

    meetings = Meeting.query.join(
        Student
    ).join(
        Schedule
    ).filter(
        Student.user_id == u_id
    ).filter(
        Schedule.date == datetime.date(
            year=int(date_parts[0]),
            month=int(date_parts[1]),
            day=int(date_parts[2])
        )
    ).all()
    return render_template(
        'day.html',
        date=date,
        meetings=meetings,
        teacher=False
    )
