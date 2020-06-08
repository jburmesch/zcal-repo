from zcal import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


association_table = db.Table('association', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'))
) 


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    first = db.Column(db.String(120), unique=True, nullable=False)
    last = db.Column(db.String(120), unique=True, nullable=False)
    utype = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    meetings = db.relationship('Meeting', secondary=association_table, back_populates='students')

    def __repr__(self):
        return f"User('{self.first}', '{self.last}', '{self.utype}', '{self.email}')"


class Meeting(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    meeting_id = db.Column(db.BigInteger, nullable=False, unique=True)
    start_time = db.Column(db.DateTime, nullable=False)
    teacher = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    students = db.relationship('User', secondary=association_table, back_populates="meetings")

    def __repr__(self):
        return f"Meeting('{self.title}','{self.start_time.date}','{self.start_time.time})"
  