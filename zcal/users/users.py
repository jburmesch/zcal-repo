from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user
from zcal import db, bcrypt
from zcal.models import User, Student, Meeting, Teacher, Schedule
import zcal.users.users_forms as forms
from zcal.admin.admin_forms import ManageForm

users = Blueprint('users', __name__)


@users.route('/user/<int:u_id>', methods=['GET', 'POST'])
@login_required
def user(u_id):
    # make sure user is the user that was submitted, or admin.
    if current_user.id == u_id or current_user.utype == 'Admin':
        user = User.query.filter(User.id == u_id).one()
        meetings = None

        name_form = forms.NameForm()
        email_form = forms.EmailForm()
        password_form = forms.PasswordForm()
        admin_form = forms.AdminForm()
        mg_form = ManageForm()

        # Forms:

        # First Name:
        if name_form.validate_on_submit() \
                and name_form.name_type.data == 'First':
            user.first = name_form.name.data
            db.session.commit()
            return redirect(url_for('users.user', u_id=u_id))
        # Last Name:
        elif name_form.validate_on_submit():
            user.last = name_form.name.data
            db.session.commit()
            return redirect(url_for('users.user', u_id=u_id))
        # Email:
        elif email_form.validate_on_submit():
            user.email = email_form.email.data
            db.session.commit()
            return redirect(url_for('users.user', u_id=u_id))
        # Password:
        elif password_form.validate_on_submit():
            pass

        # Student:

        if user.utype == 'Student':
            student = Student.query.filter(Student.user_id == u_id).one()
            meetings = Schedule.query.join(
                Meeting
            ).filter(
                Meeting.student_id == student.id
            ).all()

        # Teacher/Admin:

        elif user.utype == 'Teacher' or user.utype == 'Adimn':
            teacher = Teacher.query.filter(Teacher.user_id == u_id).one()
            schedules = Schedule.query.filter(
                Schedule.teacher_id == teacher.id
            ).all()
            meetings = []
            # look through schedules for meetings
            for schedule in schedules:
                if schedule.meeting:
                    # remove the schedule from schedules
                    # list and add to meetings
                    meetings.append(schedule)
                    schedules.remove(schedule)
            # Set meetings back to none if none are found
            if meetings == []:
                meetings = None

        return render_template(
            'user.html',
            title="User Account Management",
            user=user,
            meetings=meetings,
            name_form=name_form,
            email_form=email_form,
            password_form=password_form,
            admin_form=admin_form,
            mg_form=mg_form
        )

    # not correct user or admin
    else:
        return redirect(url_for('cal.cal'))
