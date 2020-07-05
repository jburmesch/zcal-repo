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
    teacher = db.relationship('Teacher',
                              backref=db.backref('user', uselist=False),
                              lazy=True)
    student = db.relationship('Student',
                              backref=db.backref('user', uselist=False),
                              lazy=True)
    timeslots = db.relationship('Timeslot',
                                backref='user',
                                lazy=True)

    def full_name(self):
        return f'{self.first} {self.last}'

    def __repr__(self):
        return f"<User> {self.full_name()} | {self.utype} | {self.email}"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    course_id = db.Column(
        db.Integer,
        db.ForeignKey('course.id'),
        nullable=False
    )
    # meetings = db.relationship('Meeting', backref='student', lazy=True)

    def __repr__(self):
        return f"<Student> Name: {self.user.full_name()} | "\
            + f"Email: {self.user.email} | "\
            + f"Course: {self.course.name}"


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    zoom_id = db.Column(
        db.Integer,
        db.ForeignKey('zoom.id'),
        nullable=True
    )
    time_slots = db.relationship(
        'Schedule',
        backref='teacher',
        lazy=True
    )
    zoom = db.relationship(
        'Zoom',
        backref=db.backref('teacher', uselist=False),
        lazy=True
    )

    def __repr__(self):
        if self.zoom:
            return f"<Teacher> Name: {self.user.full_name()} | "\
                + f"Email: {self.user.email} | "\
                + f"Zoom: {self.zoom.account}"
        else:
            return f"<Teacher> Name: {self.user.full_name()} | "\
                + f"Email: {self.user.email} | "


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    students = db.relationship('Student', backref='course', lazy=True)

    def __repr__(self):
        return f"<Course> Name: {self.name} | "\
            + f"Code: {self.code}"


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    student = db.relationship('Student', backref=db.backref('meetings',
                              uselist=False), lazy=True)

    def __repr__(self):
        return f"<Meeting> Date: {self.schedule.date} | "\
            + f"Time: {self.schedule.start} | "\
            + f"Teacher: {self.schedule.teacher.user.full_name()} | "\
            + f"Student: {self.student.user.full_name()}"


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    date = db.Column(db.Date, nullable=False)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'),
                           nullable=True)
    meeting = db.relationship('Meeting', backref=db.backref('schedule',
                              uselist=False), lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher': self.teacher.user.first,
            'date': str(self.date),
            'day': self.date.day,
            'start': str(self.start.isoformat(timespec='minutes')),
            'end': str(self.end.isoformat(timespec='minutes')),
            'duration': self.duration,
            'meeting': self.meeting_id
        }

    def __repr__(self):
        if self.meeting:
            return f"<Schedule> Teacher: {self.teacher.user.full_name()}, "\
                + f"Date: {self.date} | "\
                + f"Start Time: {self.start} | "\
                + f"End Time: {self.end} | "\
                + f"Duration: {self.duration} minutes |"\
                + f"Student: {self.meeting.student.user.full_name()}"
        else:
            return f"<Schedule> Teacher: {self.teacher.user.full_name()}, "\
                + f"Date: {self.date} | "\
                + f"Start Time: {self.start} | "\
                + f"End Time: {self.end} | "\
                + f"Duration: {self.duration} minutes |"\
                + "Student: None"


class Timeslot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Timeslot> Start Time: {self.start} |"\
             + f"Duration: {self.duration} minutes |"\
             + f"End Time: {self.end} |"\
             + f"Created By: {self.user.full_name()}"


class Zoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zoom_account_id = db.Column(db.String(), nullable=False)
    refresh = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Zoom> Zoom ID: {self.zoom_id} |"\
             + f"Refresh Token: {self.refresh}"
