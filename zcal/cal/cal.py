from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from zcal.cal.cal_forms import TeacherSchedule
from zcal.models import Student, Teacher, Timeslot, Schedule
from zcal import db
from datetime import date
from math import floor
import calendar


calbp = Blueprint('cal', __name__)


# make a home page someday?
@calbp.route('/')
def main():
    if current_user.is_authenticated:
        if current_user.utype == 'Admin':
            return redirect(url_for('admin.teachers'))
        else:
            return redirect(url_for('cal.cal'))
    else:
        return redirect(url_for('auth.login'))


@calbp.route('/schedule/', methods=['GET', 'POST'])
@login_required
def schedule():
    return "Not done yet."


@calbp.route('/calendar', methods=['GET', 'POST'])
@login_required
def cal(u_id=0):
    u_id = request.args.get("u_id")
    mod = request.args.get("mod")
    if not (mod and is_digit(mod)):
        mod = 0
    if current_user.utype == 'Student':
        return redirect(url_for('cal.stu_cal', u_id=current_user.id, mod=mod))
    elif current_user.utype == 'Teacher':
        return redirect(url_for('cal.t_cal', u_id=current_user.id, mod=mod))
    else:
        if Student.query.filter(Student.user_id == str(u_id)).first():
            return redirect(url_for('cal.stu_cal', u_id=u_id, mod=mod))
        elif Teacher.query.filter(Teacher.user_id == str(u_id)).first():
            return redirect(url_for('cal.t_cal', u_id=u_id, mod=mod))
        else:
            flash('User either does not exist or is admin only.',
                  "warning")
            return redirect(
                url_for('cal.t_cal', u_id=current_user.id, mod=mod)
            )


# CALENDAR ROUTE
@calbp.route('/calendar/student/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def stu_cal(u_id):
    flash('Student Calendar', 'warning')
    mod = request.args.get("mod")

    year, month = process_mod(
        date.today().year,
        date.today().month,
        mod
    )

    c = calendar.Calendar()
    caldays = c.itermonthdays2(year, month)

    return render_template(
        'calendar.html',
        caldays=caldays,
        yr=year,
        mon_num=month,
        mon=calendar.month_name[month],
        mod=mod,
        u_id=u_id,
        title='Calendar'
    )


# CALENDAR ROUTE
@calbp.route('/calendar/teacher/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def t_cal(u_id):
    flash('Teacher Calendar', 'warning')
    ts_form = TeacherSchedule()
    mod = request.args.get("mod")
    timeslots = Timeslot.query.all()
    schedules = Schedule.query.join(
        Schedule.teacher
    ).filter(
        Teacher.user_id == str(u_id)
    ).order_by(
        Schedule.date_time
    ).all()
    year, month = process_mod(
        date.today().year,
        date.today().month,
        mod
    )
    if ts_form.validate_on_submit:
        slots = ts_form.slots.data.split()
        d = ts_form.slots.data
        for slot in slots:
            start = timeslots[slot]['start']
            end = timeslots[slot]['end']
            duration = timeslots[slot]['duration']
            schedule = Schedule(
                teacher_id=u_id,
                date=d,
                start=start,
                end=end,
                duration=duration
            )
            db.session.add(schedule)
        db.session.commit()
        return (redirect(url_for(cal.cal, u_id=u_id, mod=mod)))

    c = calendar.Calendar()
    caldays = c.itermonthdays2(year, month)

    return render_template(
        'calendar.html',
        ts_form=ts_form,
        timeslots=timeslots,
        schedules=schedules,
        caldays=caldays,
        yr=year,
        mon_num=month,
        mon=calendar.month_name[month],
        mod=mod,
        u_id=u_id,
        title='Calendar'
    )


# determine whether something is a number, even if it's negative.
def is_digit(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


# improve this someday.
def process_mod(year, month, mod):
    # Mod is a modifier that simply represents the number of months
    # between the curent month and the month that should be displayed
    if not mod:
        mod = 0
    else:
        # convert mod to int
        mod = int(mod)
        # if it's negative, subtract from month and year
    if (mod < 0):
        mod = abs(mod)
        if mod >= month:
            year = year - (floor((mod - month) / 12) + 1)
            mod = mod % 12
            if mod >= month:
                month = 12 - abs(month - mod)
            else:
                month = month - mod
        else:
            month = month - mod
        # if it's positive, add to month and year
    elif mod > 0:
        if month + mod > 12:
            year = year + (floor((mod - month) / 12) + 1)
            mod = mod % 12
            if month + mod > 12:
                month = month + mod - 12
            else:
                month = month + mod
        else:
            month = month + mod
    return (year, month)
