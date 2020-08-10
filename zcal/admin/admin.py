from flask import (render_template, redirect, url_for,
                   flash, Blueprint)
from zcal import db, bcrypt
from zcal.admin.admin_forms import (
    TeacherForm, CourseForm, TimeslotForm, RemoveForm, ManageForm
)
from flask_login import login_required, current_user
from zcal.models import (
    User, Teacher, Course, Student, Timeslot, Schedule, Meeting
)
from datetime import datetime, timedelta
import secrets

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/add-teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    # Ensure that user is Admin
    if current_user.utype == "Admin":
        form = TeacherForm()
        # see if form was submitted
        if form.validate_on_submit():
            password = secrets.token_urlsafe(6)
            hashed_password = bcrypt.generate_password_hash(
                password
            ).decode('utf-8')

            user = User(
                first=form.first.data,
                last=form.last.data,
                utype="Teacher",
                email=form.email.data,
                password=hashed_password
            )

            db.session.add(user)
            db.session.commit()

            teacher = Teacher(
                user_id=user.id,
            )

            db.session.add(teacher)
            db.session.commit()

            # display success message
            flash(f'Account Created. TEMP PASS: { password }', 'success')
            return redirect(url_for('admin.add_teacher'))
        return render_template(
            'add_teacher.html',
            title='Add Teacher',
            form=form
        )
    # If not Admin:
    else:
        return redirect(url_for('cal'))


@admin.route('/teacher-management', methods=['GET', 'POST'])
@login_required
def teachers():
    if current_user.utype == "Admin":
        mg_form = ManageForm()
        rem_form = RemoveForm()
        teachers = Teacher.query.all()
        # if manage button is clicked
        if mg_form.validate_on_submit():

            u_id = Teacher.query.filter_by(
                id=mg_form.mg_id.data
            ).first().user_id

            return redirect(url_for('cal.cal', u_id=u_id))
        # if remove button is clicked
        elif rem_form.validate_on_submit():
            t_id = rem_form.rem_id.data
            teacher = Teacher.query.filter_by(id=t_id).first()
            scheds = Schedule.query.filter_by(teacher_id=t_id).all()
            meets = Meeting.query.join(
                Schedule
            ).filter(Schedule.teacher_id == t_id).all()

            # Make sure the teacher doesn't have meetings scheduled
            # with students.
            if meets:
                flash("Teacher has meetings scheduled! Reschedule before "
                      + "removing!", "error")
            else:
                if teacher:
                    user = User.query.filter_by(id=teacher.user_id).first()
                    for sched in scheds:
                        db.session.delete(sched)
                    db.session.delete(teacher)
                    db.session.delete(user)
                    db.session.commit()
                    flash("Teacher successfully removed.", "success")
                    return redirect(url_for('admin.teachers'))
                else:
                    flash("Teacher not found.", "error")
            return redirect(url_for('admin.teachers'))

        else:

            return render_template('teachers.html', title='Manage Teachers',
                                   teachers=teachers, rem_form=rem_form,
                                   mg_form=mg_form)
    else:
        return redirect(url_for('cal.cal'))


@admin.route('/default-schedule')
@login_required
def default_schedule():
    if current_user.utype == "Admin":
        return 'To be continued...'
    else:
        return redirect(url_for('cal.cal'))


@admin.route('/add-course', methods=['GET', 'POST'])
@login_required
def add_course():
    if current_user.utype == "Admin":
        form = CourseForm()
        # check for valid data
        if form.validate_on_submit():
            # add course to db
            course = Course(
                name=form.name.data,
                code=form.code.data,
            )
            db.session.add(course)
            db.session.commit()
            # display success message
            flash('Course Created.', 'success')
            return redirect(url_for('admin.add_course'))
        return render_template(
            'add_course.html',
            title='Add Course',
            form=form
        )
    else:
        return redirect(url_for('cal.cal'))


@admin.route('/course-management')
@login_required
def courses():
    if current_user.utype == "Admin":
        courses = Course.query.all()
        return render_template('courses.html', title='Manage Courses',
                               courses=courses)
    else:
        return redirect(url_for('cal.cal'))


@admin.route('/student-management')
@login_required
def students():
    if current_user.utype == "Admin":
        students = Student.query.all()
        return render_template('students.html', title='Manage Teachers',
                               students=students)
    else:
        return redirect(url_for('cal.cal'))


@admin.route('/timeslots', methods=['GET', 'POST'])
@login_required
def timeslots():
    if current_user.utype == 'Admin':
        add_form = TimeslotForm()
        rem_form = RemoveForm()
        slots = Timeslot.query.order_by(Timeslot.start).all()
        if add_form.validate_on_submit():
            end = (datetime(
                1, 1, 1, add_form.start.data.hour, add_form.start.data.minute
            ) + timedelta(minutes=add_form.duration.data)).time()
            slot = Timeslot(
                created_by=current_user.id,
                start=add_form.start.data,
                duration=add_form.duration.data,
                end=end
            )
            db.session.add(slot)
            db.session.commit()
            flash('Timeslot Added!')
            return redirect(url_for('admin.timeslots'))
        elif rem_form.validate_on_submit():
            slot = Timeslot.query.filter_by(id=rem_form.rem_id.data).first()
            if slot:
                db.session.delete(slot)
                db.session.commit()
                flash('Timeslot Removed!', 'success')
                return redirect(url_for('admin.timeslots'))
            else:
                flash('Failed to remove timeslot!', 'warning')
        else:
            return render_template(
                'timeslots.html',
                title='Manage Timeslots',
                slots=slots,
                add_form=add_form,
                rem_form=rem_form
            )
    else:
        return redirect('cal.cal')
