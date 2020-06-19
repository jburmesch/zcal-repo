from flask import (render_template, request, redirect, url_for,
                   flash, Blueprint)
from zcal import db, bcrypt
from zcal.models import User, Course, Student
from zcal.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, logout_user


auth = Blueprint('auth', __name__, url_prefix='/auth')


# REGISTER
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cal.cal'))
    form = RegistrationForm()
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
                utype="Student",
                email=form.email.data,
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            # First user to log in after db is initialized will be admin!
            if user.id == 1 and form.code.data == \
                    Course.query.filter_by(id=1).first().code:
                user.utype = 'Admin'
                db.session.commit()
            else:
                student = Student(
                    user_id=user.id,
                    course_id=Course.query.filter_by(
                        code=form.code.data
                    ).first().id
                )
                db.session.add(student)
                db.session.commit()
            # display success message
            flash('Account Created. Please check your '
                  + 'email for account validation.', 'success')
            return redirect(url_for('auth.login'))
    # display register page
    return render_template('register.html', form=form, title='Register')


# LOGIN
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cal.cal'))
    form = LoginForm()
    if form.validate_on_submit():
        # validate form and check user info
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data
        ):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main'))
        else:
            flash('Invalid email/password combination.', 'danger')
    # display login page
    return render_template('login.html', form=form, title='Login')


# LOGOUT
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('cal.main'))
