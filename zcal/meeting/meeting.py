from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import login_required
from zcal import db
from zcal.models import Meeting, Schedule

meeting = Blueprint('meeting', __name__)


@meeting.route('/meeting/<int:m_id>', methods=['GET', 'POST'])
@login_required
def mtg(m_id):
    meeting = Meeting.query.filter(Meeting.id == m_id).first()
    if not meeting:
        flash("Meeting not found.", "m")
        return redirect(url_for('cal.cal'))
    schedule = Schedule.query.filter(Schedule.meeting_id == m_id).first()
    return render_template(
        'meeting.html',
        meeting=meeting,
        schedule=schedule
    )
