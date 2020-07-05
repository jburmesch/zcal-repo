from flask import (request, redirect, url_for, Blueprint, current_app)
from zcal.cal.cal_forms import ZoomForm
from flask_login import login_required
import requests
from base64 import urlsafe_b64encode as encode64

zoom = Blueprint('zoom', __name__, url_prefix='/zoom')


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
        return z_user
    else:
        return "This isn't done yet. "
