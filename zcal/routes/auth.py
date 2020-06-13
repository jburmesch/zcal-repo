from flask import render_template, request, redirect, url_for, flash
from zcal import app, db, bcrypt
from zcal.models import User
from zcal.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, logout_user


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cal'))
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
            # display success message
            flash('Account Created. Please check your '
                  + 'email for account validation.', 'success')
            return redirect(url_for('login'))
    # display register page
    return render_template('register.html', form=form, title='Register')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cal'))
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
                redirect(url_for('cal'))
        else:
            flash('Invalid email/password combination.', 'danger')
    # display login page
    return render_template('login.html', form=form, title='Login')


# LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

