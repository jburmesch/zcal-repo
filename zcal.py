from flask import Flask, render_template, request, redirect, url_for, flash
import calendar
from datetime import date, datetime
from math import floor
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

# create app
app = Flask(__name__)
# set config variables -> switch to env variables in future
app.config['SECRET_KEY'] = 'dev'
# Secret generation:
# import secrets
# secrets.token_hex(16)
# exit

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zcal.db'
db = SQLAlchemy(app)

association_table = db.Table('association', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(120), unique=True, nullable=False)
    last = db.Column(db.String(120), unique=True, nullable=False)
    utype = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    meetings = db.relationship('Meeting', secondary=association_table, back_populates='students')

    def __repr__(self):
        return f"User('{self.first}', '{self.last}', '{self.email}')"


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    meeting_id = db.Column(db.BigInteger, nullable=False, unique=True)
    start_time = db.Column(db.DateTime, nullable=False)
    teacher = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    students = db.relationship('User', secondary=association_table, back_populates="meetings")

    def __repr__(self):
        return f"Meeting('{self.title}','{self.start_time.date}','{self.start_time.time})"
    

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
            
            # display success message
            flash(f'Account Created for {form.first.data} {form.last.data}.', 'success')
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
    # see if form was submitted
    if request.method == 'POST':
        # validate form and check user info
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash("You did it! You're logged in!", 'success')
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


if __name__ == '__main__':
    app.run(debug=True)