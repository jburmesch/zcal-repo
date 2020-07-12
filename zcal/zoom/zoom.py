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
    oauth_form = ZoomForm()
    code = request.args.get('code')
    # redirect to zoom's oauth authorization page if the form
    # was submitted.
    if oauth_form.validate_on_submit():
        return redirect(
            'https://zoom.us/oauth/authorize'
            + f'?response_type=code&client_id={current_app.config["OAUTH_ID"]}'
            + f'&redirect_uri={url_for("zoom.zoom_auth", _external=True)}'
        )
    # if the user was redirected back here with a code, use that
    # to get access and refresh codes for their account.
    if code:
        headers = auth_headers()
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
        # save the access and refresh tokens
        access = r['access_token']
        refresh = r['refresh_token']
        # make request for user info.
        z_user = requests.get(
            'https://api.zoom.us/v2/users/me',
            headers=auth_headers(access)
        ).json()
        # query db to see if the zoom account is already registered and error
        # if so.
        old_account = Zoom.query.filter_by(account=z_user['email']).first()
        if old_account:
            flash('That account has already been registered! Go to the zoom'
                  + ' homepage and log out if you\'d like to register a'
                  + 'different account.', 'danger')
            return redirect(url_for('zoom.manage'))
        # add zoom account to db
        else:
            new_account = Zoom(
                account=z_user['email'],
                zoom_account_id=z_user['id'],
                refresh=refresh,
                access=access
            )
            db.session.add(new_account)
            db.session.commit()
            flash('Zoom Account Successfully added!', 'success')
            return redirect(url_for('zoom.manage'))
    # if nothing useful was submitted
    else:
        return redirect(url_for('zoom.manage'))


# return appropriate authorization header for api authorization or request
def auth_headers(access_token=None):
    # if an access token is provided, assume it's an api request
    if access_token:
        return {
            'Authorization': 'Bearer ' + access_token
        }
    # otherwise return headers for an auth request
    else:
        o_id = current_app.config['OAUTH_ID']
        o_sec = current_app.config['OAUTH_SECRET']
        # create oauth_id:oauth_secret authorization header
        s = o_id + ':' + o_sec
        # must be 'Basic' followed by string containing base64 encoded s
        return {
            'Authorization': 'Basic ' + str(encode64(s.encode("utf-8")),
                                            "utf-8")
        }


# refresh access token (they expire after 1 hour.)
def refresh(zoom):
    # store data
    ref = zoom.refresh
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': ref
    }
    # make request
    r = requests.post(
        'https://zoom.us/oauth/token',
        data=data,
        headers=auth_headers()
    ).json()
    # store new refresh and access tokens
    zoom.refresh = r['refresh_token']
    zoom.access = r['access_token']
    # commit is important!
    db.session.commit()
    # return access token
    return r['access_token']


# add zoom meeting to zoom account via api
def schedule_zoom(schedule):
    t = schedule.teacher
    z = t.zoom
    # get a fresh access token
    access = refresh(z)
    # content of request
    data = {
        'duration': schedule.duration,
        'password': schedule.meeting.student.course.code,
        'start_time': f'{schedule.date.year}-{schedule.date.month}'
        + f'-{schedule.date.day}T{schedule.start.hour}'
        + f':{schedule.start.minute}:00',
        'timezone': 'Asia/Tokyo',
        'topic': schedule.meeting.student.course.name + ' w/ '
        + schedule.meeting.student.user.full_name(),
        'type': 2
    }
    # make request (data must be submit as json!)
    r = requests.post(
        'https://api.zoom.us/v2/users/me/meetings',
        json=data,
        headers=auth_headers(access)
    ).json()
    ''' ADD VALIDATION THAT IT WORKED '''
    print(r)
    if r['uuid']:
        flash('Zoom meeting created!', 'success')
    else:
        flash(
            'Zoom meeting creation failed!, please contact administrator!',
            'danger'
        )
