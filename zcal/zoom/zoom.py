from flask import (
    request, redirect, url_for, Blueprint, current_app, flash, render_template
)
from zcal.zoom.zoom_forms import ZoomForm, ZoomlessTeachers
from zcal.admin.admin_forms import RemoveForm
from zcal.models import Zoom, Teacher
from zcal import db
from flask_login import login_required
import requests
from base64 import urlsafe_b64encode as encode64

zoom = Blueprint('zoom', __name__, url_prefix='/zoom')


@zoom.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    oauth_form = ZoomForm()
    rem_form = RemoveForm()
    zl_teachers = Teacher.query.filter_by(zoom=None).all()
    t_form = ZoomlessTeachers()
    t_form.teachers.choices = [(t.id, t.user.full_name()) for t in zl_teachers]
    zooms = Zoom.query.all()
    if t_form.validate_on_submit():
        t = Teacher.query.filter_by(id=t_form.teachers.data).first()
        t.zoom_id = t_form.zm_id.data
        db.session.commit()
    return render_template(
        'zoom.html',
        t_form=t_form,
        oauth_form=oauth_form,
        zooms=zooms,
        rem_form=rem_form
    )


@zoom.route('/zoom-auth', methods=['GET', 'POST'])
@login_required
def zoom_auth():
    o_id = current_app.config['OAUTH_ID']
    o_sec = current_app.config['OAUTH_SECRET']
    oauth_form = ZoomForm()
    code = request.args.get('code')
    # redirect to zoom's oauth authorization page if the form
    # was submitted.
    if oauth_form.validate_on_submit():
        return redirect(
            'https://zoom.us/oauth/authorize'
            + f'?response_type=code&client_id={o_id}'
            + f'&redirect_uri={url_for("zoom.zoom_auth", _external=True)}'
        )
    # if the user was redirected back here with a code, use that
    # to get access and refresh codes for their account.
    if code:
        # create oauth_id:oauth_secret authorization header
        s = o_id + ':' + o_sec
        # must be 'Basic' followed by string containing base64 encoded s
        headers = {
            'Authorization': 'Basic ' + str(encode64(s.encode("utf-8")),
                                            "utf-8")
        }
        # prepare data for request
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': url_for('zoom.zoom_auth', _external=True)
        }
        # request token
        r = requests.post(
            'https://zoom.us/oauth/token',
            data=data,
            headers=headers,
        ).json()
        access = r['access_token']
        refresh = r['refresh_token']
        z_user = requests.get(
            'https://api.zoom.us/v2/users/me',
            headers={'Authorization': 'Bearer ' + access}
        ).json()
        old_account = Zoom.query.filter_by(account=z_user['email']).first()
        if old_account:
            flash('That account has already been registered! Go to the zoom'
                  + ' homepage and log out if you\'d like to register a'
                  + 'different account.', 'danger')
            return redirect(url_for('zoom.manage'))
        else:
            new_account = Zoom(
                account=z_user['email'],
                zoom_account_id=z_user['id'],
                refresh=refresh
            )
            db.session.add(new_account)
            db.session.commit()
            flash('Zoom Account Successfully added!', 'success')
            return redirect(url_for('zoom.manage'))
    else:
        return redirect(url_for('zoom.manage'))
