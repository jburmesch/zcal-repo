from zcal import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    first = db.Column(db.String(120), nullable=False)
    last = db.Column(db.String(120), nullable=False)
    utype = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    teacher = db.relationship('Teacher', backref='user', lazy=True)
    meetings = db.relationship('Meeting', backref='user', lazy=True)

    def full_name(self):
        return f'{self.first} {self.last}'

    def __repr__(self):
        return f"<User> {self.first} {self.last}| {self.utype}| {self.email}"


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                           nullable=False)
    # schedule = db.relationship('Schedule', lazy=True, uselist=False)

    def __repr__(self):
        return f"<Meeting> Date: {self.schedule.date_time.date()}, "\
            + f"Time: {self.schedule.date_time.time()}, "\
            + f"Teacher: {self.schedule.teacher.user.full_name()}, "\
            + f"Student: {self.user.full_name()})"


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    zoom_id = db.Column(db.Integer, db.ForeignKey('zoom.id'), nullable=True)
    time_slots = db.relationship('Schedule', backref='teacher', lazy=True)

    def __repr__(self):
        return f"<Teacher> Name: {self.user.full_name()}"


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'),
                           nullable=True)
    meeting = db.relationship('Meeting', backref=db.backref('schedule',
                              uselist=False), lazy=True)

    def __repr__(self):
        if self.meeting:
            return f"<Schedule> Teacher: {self.teacher.user.full_name()}, "\
                + f"Date: {self.date_time.date()}, "\
                + f"Time: {self.date_time.time()}, "\
                + f"Student: {self.meeting.user.full_name()})"
        else:
            return f"<Schedule> Teacher: {self.teacher.user.full_name()}, "\
                + f"Date: {self.date_time.date()}, "\
                + f"Time: {self.date_time.time()}, "\
                + "Student: None"


class Zoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Zoom Info> Account: {self.account}"
