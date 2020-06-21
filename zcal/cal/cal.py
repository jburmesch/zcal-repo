from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from zcal.cal.cal_forms import ScheduleForm
from zcal.models import Student, Teacher
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
        if Student.query.filter_by(user_id=u_id).first():
            return redirect(url_for('cal.stu_cal', u_id=u_id, mod=mod))
        elif Teacher.query.filter_by(user_id=u_id).first():
            return redirect(url_for('cal.t_cal', u_id=u_id, mod=mod))
        else:
            flash('User either does not exist or is admin only.',
                  "warning")
            return redirect(
                url_for('cal.t_cal', u_id=current_user.id, mod=mod)
            )


# CALENDAR ROUTE
@calbp.route('/calendar/user-<int:u_id>', methods=['GET', 'POST'])
@login_required
def stu_cal(u_id):
    mod = request.args.get("mod")
    form = ScheduleForm()

    year, month = process_mod(
        date.today().year,
        date.today().month,
        mod
    )

    c = calendar.Calendar()
    caldays = c.itermonthdays2(year, month)

    return render_template(
        'calendar.html',
        form=form,
        caldays=caldays,
        yr=year,
        mon_num=month,
        mon=calendar.month_name[month],
        mod=mod,
        u_id=u_id,
        title='Calendar'
    )


# CALENDAR ROUTE
@calbp.route('/calendar/user-<int:u_id>', methods=['GET', 'POST'])
@login_required
def t_cal(u_id):
    mod = request.args.get("mod")
    form = ScheduleForm()

    year, month = process_mod(
        date.today().year,
        date.today().month,
        mod
    )

    c = calendar.Calendar()
    caldays = c.itermonthdays2(year, month)

    return render_template(
        'calendar.html',
        form=form,
        caldays=caldays,
        yr=year,
        mon_num=month,
        mon=calendar.month_name[month],
        mod=mod,
        u_id=u_id,
        title='Calendar'
    )


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
        mod = int(mod)
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
