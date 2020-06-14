from flask import render_template, request, redirect, url_for
from zcal import app
from flask_login import login_required, current_user


@app.route('/admin')
@login_required
def admin():
    if current_user.utype == "Admin":
        return "You're an admin, but this page isn't done yet."
    else:
        return 'Not done yet.'
