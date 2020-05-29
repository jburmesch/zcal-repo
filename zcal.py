from flask import Flask, render_template, request, redirect, url_for, flash
import calendar
from datetime import date
from math import floor
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'

# Secret generation:
# import secrets
# secrets.token_hex(16)
# exit

meetings = [
    {
        'title': 'Counseling with Takako',
        'year': 2020,
        'month': 5,
        'day':15,
        'time': '15:00'

    }
]

@app.route('/')
def main():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(f'Account Created for {form.first.data} {form.last.data}.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash("You did it! You're logged in!", 'success')
            return redirect(url_for('cal'))
        else:
            flash('Invalid email/password combination.', 'danger')
    return render_template('login.html', form=form, title='Login')


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


if __name__ == '__main__':
    app.run(debug=True)