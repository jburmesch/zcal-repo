from flask import (
    render_template, request, redirect, url_for, Blueprint, flash, current_app
) 
from flask_login import login_required, current_user
from zcal.cal.cal_forms import TeacherSchedule, ZoomForm
from zcal.models import Student, Teacher, Timeslot, Schedule, User, Meeting
from zcal import db
from datetime import date
from math import floor
import calendar
import simplejson as json


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


@calbp.route('/zoom-auth', methods=['GET', 'POST'])
@login_required
def zoom_auth():
    o_id = current_app.config['OAUTH_ID']
    oauth_form = ZoomForm()
    code = request.args.get('code')
    if oauth_form.validate_on_submit():
        return redirect("https://zoom.us/oauth/authorize"
                        + f"?response_type=code&client_id={o_id}"
                        + f"&redirect_uri={url_for('cal.zoom_auth', _external=True)}")
    if code:
        return code
    else:
        return "This isn't done yet. "


@calbp.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    return "Not done yet."


@calbp.route('/calendar', methods=['GET', 'POST'])
@login_required
def cal(u_id=0):
    u_id = request.args.get("u_id")
    mod = request.args.get("mod")
    # if there's no month modifier, set it to 0.
    if not (mod and is_digit(mod)):
        mod = 0
    # redirect for students
    if current_user.utype == 'Student':
        return redirect(url_for('cal.stu_cal', u_id=current_user.id, mod=mod))
    # redirect for teachers
    elif current_user.utype == 'Teacher':
        return redirect(url_for('cal.t_cal', u_id=current_user.id, mod=mod))
    # for admins, return calendar based on the type of user they're looking up.
    else:
        # student
        if Student.query.filter(Student.user_id == str(u_id)).first():
            return redirect(url_for('cal.stu_cal', u_id=u_id, mod=mod))
        # teacher
        elif Teacher.query.filter(Teacher.user_id == str(u_id)).first():
            return redirect(url_for('cal.t_cal', u_id=u_id, mod=mod))
        # original admin doesn't have a meaningful calendar, but
        # if they look themself up, we'll show them one anyway I guess.
        else:
            flash('User either does not exist or is admin only.',
                  "warning")
            return redirect(
                url_for('cal.t_cal', u_id=current_user.id, mod=mod)
            )


# Student calendar route - for scheduling meetings with available teachers
@calbp.route('/calendar/student/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def stu_cal(u_id):
    mod = request.args.get("mod")
    # ADD VALIDATION TO THIS!
    if request.method == 'POST':
        # CHECK THAT ID IS INT AND IN SCHED LIST!
        sched = Schedule.query.filter_by(id=request.form.get("time_list")).first()
        mtg = Meeting(
            student_id=u_id,
        )
        db.session.add(mtg)
        db.session.commit()
        sched.meeting_id = mtg.id
        db.session.commit()

    # figure out which month should be displayed based on the current date
    # and the month modifier.
    year, month = process_mod(
        date.today().year,
        date.today().month,
        mod
    )
    schedules = Schedule.query.filter(
        Schedule.date >= date(date.today().year, month, 1),
        Schedule.date < date(date.today().year, month + 1, 1),
        Schedule.meeting_id == None  # noqa
    ).all()

    sched_json = get_json(schedules)

    a_dict = {}

    for sched in schedules:
        d = sched.date.day
        if d in a_dict.keys():
            a_dict[d] += 1
        else:
            a_dict[d] = 1
    # create calendar object and list of days.
    c = calendar.Calendar()
    caldays = c.itermonthdays2(year, month)
    # return the template
    return render_template(
        'calendar.html',
        caldays=caldays,
        yr=year,
        mon_num=month,
        mon=calendar.month_name[month],
        mod=mod,
        u_id=u_id,
        title='Calendar',
        schedules=schedules,
        a_dict=a_dict,
        sched_json=sched_json
    )


# Teacher calendar, for managing teacher meetings and availability.
@calbp.route('/calendar/teacher/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def t_cal(u_id):
    ts_form = TeacherSchedule()
    oauth_form = ZoomForm()
    mod = request.args.get("mod")
    # figure out which month should be displayed based on the current date
    # and the month modifier.
    year, month = process_mod(
        date.today().year,
        date.today().month,
        mod
    )

    # get all timeslots from db.
    timeslots = Timeslot.query.all()
    schedules = Schedule.query.join(
        Teacher
    ).filter(
        Teacher.user_id == str(u_id),
        Schedule.date >= date(date.today().year,
                              month, 1),
        Schedule.date < date(date.today().year,
                             month + 1, 1)
    ).order_by(
        Schedule.date,
        Schedule.start,
        Schedule.duration
    ).all()
    a_dict = {}
    m_dict = {}
    for sched in schedules:
        if sched.meeting_id:
            d = sched.date.day
            t = User.query.filter(User.id == u_id).first().full_name()
            dt = sched.date
            st = sched.start
            et = sched.end
            stu = sched.meeting.student.user.full_name()
            dur = sched.duration
            if d in m_dict.keys():
                pass
            else:
                m_dict[d] = {
                    'date': dt,
                    'start': st,
                    'end': et,
                    'duration': dur,
                    'student': stu,
                    'teacher': t
                }
        else:
            d = sched.date.day
            if d in a_dict.keys():
                a_dict[d] += 1
            else:
                a_dict[d] = 1

    # TIMESLOT FORM SUBMISSION
    if ts_form.is_submitted():
        # parse timeslots that have been submitted
        slots = ts_form.slots.data.split()
        d = ts_form.date.data
        # add each timeslot to the db.
        for slot in slots:
            start = timeslots[int(slot) - 1].start
            end = timeslots[int(slot) - 1].end
            duration = timeslots[int(slot) - 1].duration
            tid = Teacher.query.filter(
                Teacher.user_id == u_id
            ).first().id

            schedule = Schedule(
                teacher_id=tid,
                date=d,
                start=start,
                end=end,
                duration=duration
            )
            db.session.add(schedule)
        db.session.commit()
        # redirect back to same page.
        return (redirect(url_for('cal.cal', u_id=u_id, mod=mod)))
    # create calendar object and list of days.
    c = calendar.Calendar()
    caldays = c.itermonthdays2(year, month)
    # generate template
    return render_template(
        'calendar.html',
        ts_form=ts_form,
        oauth_form=oauth_form,
        timeslots=timeslots,
        schedules=schedules,
        caldays=caldays,
        yr=year,
        mon_num=month,
        mon=calendar.month_name[month],
        mod=mod,
        u_id=u_id,
        a_dict=a_dict,
        m_dict=m_dict,
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


def get_json(schedules):
    # key = day number, value = teacher dict
    sched_dict = {}
    for sched in schedules:
        d = 'd' + str(sched.date.day)
        t = sched.teacher.id
        if sched_dict.get(d) and sched_dict[d].get(t):
            sched_dict[d][t].append(sched.to_dict())
        elif sched_dict.get(d):
            sched_dict[d].update({t: [sched.to_dict()]})
        else:
            sched_dict[d] = {t: [sched.to_dict()]}
    return json.dumps(sched_dict)
