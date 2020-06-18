from flask import render_template, redirect, url_for, request, flash
from zcal import app, db, bcrypt
from zcal.forms import TeacherForm, CourseForm
from flask_login import login_required, current_user
from zcal.models import User, Teacher, Course, Student
import secrets


@app.route('/add-teacher', methods=['GET', 'POST'])
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
                return redirect(url_for('add_teacher'))
        return render_template(
            'add_teacher.html',
            title='Add Teacher',
            form=form
        )
    else:
        return redirect(url_for('cal'))


@app.route('/teacher-management')
@login_required
def teachers():
    if current_user.utype == "Admin":
        teachers = Teacher.query.all()
        return render_template('teachers.html', title='Manage Teachers',
                               teachers=teachers)
    else:
        return redirect(url_for('cal'))


@app.route('/schedule-management')
@login_required
def base_schedule():
    if current_user.utype == "Admin":
        return 'To be continued...'
    else:
        return redirect(url_for('cal'))


@app.route('/add-course', methods=['GET', 'POST'])
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
            return redirect(url_for('add_course'))
        return render_template(
            'add_course.html',
            title='Add Course',
            form=form
        )
    else:
        return redirect(url_for('cal'))


@app.route('/course-management')
@login_required
def courses():
    if current_user.utype == "Admin":
        courses = Course.query.all()
        return render_template('courses.html', title='Manage Courses',
                               courses=courses)
    else:
        return redirect(url_for('cal'))


@app.route('/student-management')
@login_required
def students():
    if current_user.utype == "Admin":
        students = Student.query.all()
        return render_template('students.html', title='Manage Teachers',
                               students=students)
    else:
        return redirect(url_for('cal'))
