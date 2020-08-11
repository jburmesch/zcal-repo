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
            # Create password for the new teacher
            password = secrets.token_urlsafe(6)
            # hash it.
            hashed_password = bcrypt.generate_password_hash(
                password
            ).decode('utf-8')

            # create user
            user = User(
                first=form.first.data,
                last=form.last.data,
                utype="Teacher",
                email=form.email.data,
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()

            # create teacher
            teacher = Teacher(
                user_id=user.id,
            )
            db.session.add(teacher)
            db.session.commit()

            # display success message
            '''Display of temp password is TEMPORARY!
            Eventually want to send an email to teacher.'''
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

        # manage form
        if mg_form.validate_on_submit():
            # query the database for teacher who was selected
            u_id = Teacher.query.filter_by(
                id=mg_form.mg_id.data
            ).first().user_id
            # display that user's calendar
            return redirect(url_for('cal.cal', u_id=u_id))
        
        # remove form
        elif rem_form.validate_on_submit():
            # store teacher id sent from removal form
            t_id = rem_form.rem_id.data
            # get teacher from db.
            teacher = Teacher.query.filter_by(id=t_id).first()
            # get all of their open meeting slots
            scheds = Schedule.query.filter_by(teacher_id=t_id).all()
            # and all of their scheduled meetings
            meets = Meeting.query.join(
                Schedule
            ).filter(Schedule.teacher_id == t_id).all()

            if meets:
                flash("Teacher has meetings scheduled! Reschedule before "
                      + "removing!", "error")
            else:
                # make sure that a teacher was actually found in the db
                if teacher:
                    # find user in db.
                    user = User.query.filter_by(id=teacher.user_id).first()
                    # delete all of users open schedule slots
                    for sched in scheds:
                        db.session.delete(sched)
                    # delete teacher
                    db.session.delete(teacher)
                    # delete user
                    db.session.delete(user)
                    db.session.commit()

                    # report success.
                    flash("Teacher successfully removed.", "success")
                    return redirect(url_for('admin.teachers'))
                else:
                    flash("Teacher not found.", "error")
            return redirect(url_for('admin.teachers'))
        # if no form was submitted:
        else:
            return render_template('teachers.html', title='Manage Teachers',
                                   teachers=teachers, rem_form=rem_form,
                                   mg_form=mg_form)
    # if not admin:
    else:
        return redirect(url_for('cal.cal'))


@admin.route('/add-course', methods=['GET', 'POST'])
@login_required
def add_course():
    if current_user.utype == "Admin":
        form = CourseForm()

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
        # form not submitted:
        return render_template(
            'add_course.html',
            title='Add Course',
            form=form
        )
    # not admin:
    else:
        return redirect(url_for('cal.cal'))


@admin.route('/course-management', methods=['GET', 'POST'])
@login_required
def courses():
    if current_user.utype == "Admin":
        courses = Course.query.all()
        rem_form = RemoveForm()
        mg_form = ManageForm()

        # remove form
        if rem_form.validate_on_submit():
            c_id = rem_form.rem_id.data
            # get course from db
            c = Course.query.filter(Course.id == c_id).first()
            # get course's students
            students = Student.query.filter(Student.course_id == c_id).all()
            if students:
                flash(
                    'This course can not be removed while it'
                    + ' has students attached to it.', "error"
                )
            # no students:
            else:
                db.session.delete(c)
                db.session.commit()
                flash("Course Deleted.", "success")
                return redirect(url_for('admin.courses'))

        # manage form
        if mg_form.validate_on_submit():
            c_id = mg_form.mg_id.data
            c = Course.query.filter(Course.id == c_id).first()
            students = Student.query.filter(Student.course_id == c_id).all()
            return render_template(
                'students.html',
                title=f'{c.name}: Student Management',
                students=students,
                course=c
            )

        # no form submitted
        return render_template(
            'courses.html',
            title='Manage Courses',
            courses=courses,
            rem_form=rem_form,
            mg_form=mg_form
        )
    # not admin:
    else:
        return redirect(url_for('cal.cal'))


@admin.route('/student-management')
@login_required
def students():
    if current_user.utype == "Admin":
        students = Student.query.all()
        return render_template('students.html', title='Manage Teachers',
                               students=students)
    # not admin:
    else:
        return redirect(url_for('cal.cal'))


@admin.route('/timeslots', methods=['GET', 'POST'])
@login_required
def timeslots():
    if current_user.utype == 'Admin':
        add_form = TimeslotForm()
        rem_form = RemoveForm()
        slots = Timeslot.query.order_by(Timeslot.start).all()

        # add form is submit
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

        # remove form is submitted
        elif rem_form.validate_on_submit():
            slot = Timeslot.query.filter_by(id=rem_form.rem_id.data).first()
            if slot:
                db.session.delete(slot)
                db.session.commit()
                flash('Timeslot Removed!', 'success')
                return redirect(url_for('admin.timeslots'))
            else:
                flash('Failed to remove timeslot!', 'warning')

        # no form is submitted
        else:
            return render_template(
                'timeslots.html',
                title='Manage Timeslots',
                slots=slots,
                add_form=add_form,
                rem_form=rem_form
            )
    # not admin:
    else:
        return redirect('cal.cal')
