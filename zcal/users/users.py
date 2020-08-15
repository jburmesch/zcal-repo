from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user
from zcal.models import User

users = Blueprint('users', __name__)


@users.route('/user/<int:u_id>')
@login_required
def user(u_id):
    # make sure user is the user that was submitted, or admin.
    if current_user.id == u_id or current_user.utype == 'Admin':
        user = User.query.filter(User.id == u_id).one()
        return render_template(
            'user.html',
            user=user
        )
    # not correct user or admin
    else:
        return redirect(url_for('cal.cal'))
