from zcal import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    first = db.Column(db.String(120), unique=True, nullable=False)
    last = db.Column(db.String(120), unique=True, nullable=False)
    utype = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    teacher_meetings = db.relationship('Meeting', backref='teacher', lazy=True, foreign_keys= 'Meeting.teacher_id')
    student_meetings = db.relationship('Meeting', backref='student', lazy=True, foreign_keys= 'Meeting.student_id')
    

    def __repr__(self):
        return f"<User> {self.first} {self.last}, {self.utype}, {self.email})"


class Meeting(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    

    def __repr__(self):
        return f"<Meeting> Date: {self.date_time.date}, Time: {self.date_time.time}, Teacher: {self.teacher.first} {self.teacher.last}, Student: {self.student.first} {self.student.last})"
