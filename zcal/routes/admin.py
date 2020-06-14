from flask import render_template, redirect, url_for
from zcal import app
from zcal.forms import TeacherForm
from flask_login import login_required, current_user


@app.route('/add-teacher')
@login_required
def add_teacher():
    if current_user.utype == "Admin":
        form = TeacherForm()
        # see if form was submitted
        if request.method == 'POST':
            # check for valid data
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data
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
                # display success message
                flash('Account Created. Teacher will be sent an '
                    + 'email for password creation.', 'success')
                return redirect(url_for('cal'))
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
        return render_template('teachers.html', title='Manage Teachers')
    else:
        return redirect(url_for('cal'))


@app.route('/student-management')
@login_required
def students():
    if current_user.utype == "Admin":
        return render_template('students.html', title='Manage Students')
    else:
        return redirect(url_for('cal'))
