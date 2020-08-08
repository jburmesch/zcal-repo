from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import login_required
from zcal import db
from zcal.admin.admin_forms import RemoveForm, ManageForm
from zcal.models import Meeting, Student, Schedule, Teacher
import datetime


day = Blueprint('day', __name__)


@day.route('/teacher/<string:date>/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def t_meetings(date, u_id):
    # split date into year month and day
    date_parts = date.split("-")
    # create forms
    mg_form = ManageForm()
    rem_form = RemoveForm()

    # remove timeslot when remove form is submitted.
    if rem_form.validate_on_submit():
        r_sched = Schedule.query.filter(
            Schedule.id == rem_form.rem_id.data
        ).first()
        db.session.delete(r_sched)
        db.session.commit()
        flash('Timeslot removed!', 'success')
    # redirect to meeting management page
    elif mg_form.validate_on_submit():
        m_id = mg_form.mg_id.data
        return redirect(url_for('day.manage_meeting', mtg_id=m_id))

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
        mg_form=mg_form,
        rem_form=rem_form
    )


@day.route('/student/<string:date>/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def s_meetings(date, u_id):
    # split the date into year month and day
    date_parts = date.split("-")

    # create forms
    rem_form = RemoveForm()
    mg_form = ManageForm()

    if mg_form.validate_on_submit():
        m_id = mg_form.mg_id.data
        return redirect(url_for('day.manage_meeting', mtg_id=m_id))

    # get all meetings for the current user that match the date.
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
        teacher=False,
        rem_form=rem_form,
        mg_form=mg_form
    )


@day.route('/student/meeting/mtg<int:mtg_id>', methods=['GET', 'POST'])
@login_required
def manage_meeting(mtg_id):
    meeting = Meeting.query.filter(Meeting.id == mtg_id).first()
    print(meeting)
    return render_template(
        'manage_meeting.html',
        meeting=meeting
    )
