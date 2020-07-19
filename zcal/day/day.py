from flask import (render_template, Blueprint)
from flask_login import login_required
from zcal.models import Meeting, Student, Schedule, Teacher
import datetime


day = Blueprint('day', __name__)


@day.route('/teacher/<string:date>/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def t_meetings(date, u_id):
    date_parts = date.split("-")

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
        schedules=schedules
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
        meetings=meetings
    )
