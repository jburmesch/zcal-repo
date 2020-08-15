from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user
from zcal.models import User, Student, Meeting, Teacher, Schedule

users = Blueprint('users', __name__)


@users.route('/user/<int:u_id>')
@login_required
def user(u_id):
    # make sure user is the user that was submitted, or admin.
    if current_user.id == u_id or current_user.utype == 'Admin':
        user = User.query.filter(User.id == u_id).one()
        if user.utype == 'Student':
            student = Student.query.filter(Student.user_id == u_id).one()
            meetings = Meeting.query.filter(
                Meeting.student_id == student.id
            ).all()
        elif user.utype == 'Teacher' or user.utype == 'Adimn':
            teacher = Teacher.query.filter(Teacher.user_id == u_id).one()
            schedules = Schedule.query.filter(Schedule.teacher_id == teacher.id).one()
            meetings = []

        return render_template(
            'user.html',
            title="User Account Management",
            user=user,
            meetings=meetings
        )
    # not correct user or admin
    else:
        return redirect(url_for('cal.cal'))
