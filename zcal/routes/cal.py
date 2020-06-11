from flask import Flask, render_template, request, redirect, url_for, flash
from zcal import app, db, bcrypt
from zcal.models import User, Meeting
from flask_login import current_user
from zcal.forms import ScheduleForm
from datetime import date
from math import floor
import calendar

# make a home page someday?
@app.route('/')
def main():
    return redirect(url_for('login'))


@app.route('/schedule', methods=['POST'])
def schedule():
    if form.validate_on_submit():
        flash('okay!', 'success')
    return redirect(url_for('cal'))


# CALENDAR ROUTE
@app.route('/calendar', methods=['GET', 'POST'])
def cal():
    mod = request.args.get("mod")
    year=date.today().year 
    month=date.today().month
    form=ScheduleForm()

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
    return render_template('calendar.html', form=form, caldays=caldays, yr=year, mon_num=month, mon=calendar.month_name[month], mod=o_mod, title='Calendar')

