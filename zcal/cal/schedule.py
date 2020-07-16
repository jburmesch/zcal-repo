from flask import (render_template, Blueprint)
from flask_login import login_required
from zcal.models import Meeting, Schedule


schedule = Blueprint('schedule', __name__, url_prefix='/schedule')


@schedule.route('/teacher/<str:date>/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def t_meetings(date, u_id):
    return render_template(
        'schedule.html',
        meetings=None,
        schedules=None
    )


@schedule.route('/student/<str:date>/u<int:u_id>', methods=['GET', 'POST'])
@login_required
def s_meetings(date, u_id):
    meetings = Meeting.filter(Meeting.student.user_id == u_id).all()
    return render_template(
        'schedule.html',
        meetings=meetings
    )
