from flask import (render_template, redirect, url_for, request,
                   flash, Blueprint)
from zcal import db, bcrypt
from zcal.admin.admin_forms import (
    TeacherForm, CourseForm, TimeslotForm, RemoveForm
)
from flask_login import login_required, current_user
from zcal.models import User, Teacher, Course, Student, Timeslot
from datetime import datetime, timedelta
import secrets

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/add-teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    if current_user.utype == "Admin":
        form = TeacherForm()
        # see if form was submitted
        if request.method == 'POST':
            # check for valid data
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
    else:
        return redirect(url_for('cal'))


@admin.route('/teacher-management')
@login_required
def teachers():
    if current_user.utype == "Admin":
        teachers = Teacher.query.all()
        return render_template('teachers.html', title='Manage Teachers',
                               teachers=teachers)
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
            return redirect(url_for('cal.add_course'))
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
        if add_form.add.data and add_form.validate():
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
        elif rem_form.remove.data and rem_form.validate():
            slot = Timeslot.query.filter_by(id=rem_form.item_id.data).first()
            if slot:
                db.session.delete(slot)
                db.session.commit()
                flash('Timeslot Removed!')
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
