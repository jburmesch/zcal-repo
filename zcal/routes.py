from flask import Flask, render_template, request, redirect, url_for, flash
from zcal import app, db, bcrypt
from zcal.forms import RegistrationForm, LoginForm
from zcal.models import User, Meeting
from flask_login import login_user, current_user
from datetime import date
from math import floor
import calendar

# make a home page someday?
@app.route('/')
def main():
    return redirect(url_for('login'))

# REGISTER ROUTE
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # see if form was submitted
    if request.method == 'POST':
        # check for valid data
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(first=form.first.data, last=form.last.data, utype = "Student", email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            # display success message
            flash(f'Account Created. Please check your email for account validation.', 'success')
            return redirect(url_for('login'))
    # display register page
    return render_template('register.html', form=form, title='Register')


@app.route('/redirect', methods=['GET', 'POST'])
def get_token():
    return redirect(url_for('main'))


# LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # validate form and check user info
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('cal'))
        else:
            flash('Invalid email/password combination.', 'danger')
    # display login page
    return render_template('login.html', form=form, title='Login')


# CALENDAR ROUTE
@app.route('/calendar', methods=['GET', 'POST'])
def cal():
    mod = request.args.get("mod")
    year=date.today().year 
    month=date.today().month
    # improve this someday.
    if not mod:
        mod = 0
    else:
        mod = int(mod)
    o_mod = mod
    if (mod < 0):
        mod = abs(mod)
        if mod >= month:
            year = year - (floor((mod - month) / 12) + 1)
            mod = mod % 12
            if mod >= month:
                month = 12 - abs(month - mod)
            else:
                month = month - mod
        else:
            month = month - mod
    elif mod > 0:
        if month + mod > 12:
            year = year + (floor((mod - month) / 12) + 1)
            mod = mod % 12
            if month + mod > 12:
                month = month + mod - 12
            else:
                month = month + mod
        else: 
            month = month + mod
    
    c = calendar.Calendar()
    caldays =  c.itermonthdays2(year, month)
    return render_template('calendar.html', caldays=caldays, yr=year, mon=calendar.month_name[month], mod=o_mod, title='Calendar')

