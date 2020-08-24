from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from zcal import db, bcrypt
from zcal.models import User, Student, Meeting, Teacher, Schedule, Course
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
        form = None
        course = None

        name_form = forms.NameForm()
        email_form = forms.EmailForm()
        password_form = forms.PasswordForm()
        admin_form = forms.AdminForm()
        mg_form = ManageForm()

        # Student:

        if user.utype == 'Student':
            student = Student.query.filter(Student.user_id == u_id).first()
            if student is None:
                flash('Student not found', 'warning')
                course = None
            else:
                course = student.course
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

        # Forms:

        # First Name:
        if name_form.validate_on_submit() \
                and name_form.name_type.data == 'First':
            form = 'First'
            user.first = name_form.name.data
            db.session.commit()
            return redirect(url_for('users.user', u_id=u_id))
        # Last Name:
        elif name_form.validate_on_submit():
            form = 'Last'
            user.last = name_form.name.data
            db.session.commit()
            return redirect(url_for('users.user', u_id=u_id))
        # Email:
        elif email_form.validate_on_submit():
            form = 'Email'
            user.email = email_form.email.data
            db.session.commit()
            return redirect(url_for('users.user', u_id=u_id))
        # Password:
        elif password_form.validate_on_submit():
            form = 'Password'
            hashed_password = bcrypt.generate_password_hash(
                password_form.new_password.data
            ).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('users.user', u_id=u_id))
        # Admin:
        elif admin_form.validate_on_submit():
            form = 'Admin'

            # Change user to Student
            if admin_form.utype.data != 'Change' \
                    and admin_form.utype.data != user.utype:
                # make sure a course was provided
                if admin_form.utype.data == 'Student'\
                        and admin_form.utype.data is None:
                    flash('Students must be attached to a course.', 'error')
                    return redirect(url_for('users.user', u_id=u_id))
                elif admin_form.utype.data == 'Student'\
                        and user.utype != 'Student':
                    # find the user's teacher entry
                    teacher = Teacher.query.filter(
                        Teacher.user_id == user.id
                    ).one()
                    # make sure that a teacher entry is found
                    if teacher is None:
                        flash('Teacher not found.', 'error')
                        # return redirect(url_for('users.user', u_id=u_id))
                    # make sure they don't have meetings scheduled
                    if meetings:
                        flash(
                            'Cannot change user type while user has meetings '
                            + 'scheduled.', 'error'
                        )
                        return redirect(url_for('users.user', u_id=u_id))
                    # If everything's okay...
                    db.session.delete(teacher)
                    # find course
                    course = Course.query.filter(
                        Course.code == admin_form.code.data
                    ).one()
                    # create student entry:
                    student = Student(
                        user_id=u_id,
                        course_id=admin_form.code.data
                    )
                    db.session.add(student)
                    # change user type
                    user.utype = 'Student'
                    db.session.commit()
                    flash(
                        'User changed to Student.  Course set to '
                        + f'{course.name}.', "success"
                    )

            # Change student's course:
            elif admin_form.utype.data == user.utype \
                    or admin_form.utype.data == 'Change' \
                    and user.utype == 'Student' \
                    and admin_form.code.data != course.code:
                c_id = Course.query.filter(
                    Course.code == admin_form.code.data
                ).one().id
                if student:
                    student.course_id = c_id
                else:
                    student = Student(
                        user_id=u_id,
                        course_id=c_id
                    )
                    db.session.add(student)
                db.session.commit()
                flash('Course Changed.', 'success')
                return redirect(url_for('users.user', u_id=u_id))

        # Generate Template
        return render_template(
            'user.html',
            title="User Account Management",
            user=user,
            meetings=meetings,
            name_form=name_form,
            email_form=email_form,
            password_form=password_form,
            admin_form=admin_form,
            mg_form=mg_form,
            form=form,
            course=course
        )

    # not correct user or admin
    else:
        return redirect(url_for('cal.cal'))
