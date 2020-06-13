from zcal import db
from zcal.models import User, Teacher, Meeting, Schedule, Zoom
import datetime


def main():
    answer = input("RUNNING THIS WILL **DROP** ANY EXISTING DB TABLES! "
                   + "Are you sure?")
    if answer == 'y':
        db.drop_all()
        db.create_all()

        users = create_users()
        teacher = create_teacher()py
        schedule = create_schedule()
        zoom = create_zoom()
        meeting = create_meeting()

        for user in users:
            db.session.add(user)
        db.session.commit()
        print(User.query.all())

        db.session.add(teacher)
        db.session.commit()
        print(Teacher.query.all())

        db.session.add(meeting)
        db.session.commit()

        db.session.add(schedule)
        db.session.commit()
        print(Meeting.query.all())
        print(Schedule.query.all())

        db.session.add(zoom)
        db.session.commit()
        print(Zoom.query.all())

        db.drop_all()
        db.create_all()
    else:
        print('Whew. Crisis averted.')


def create_users():
    users = [
        User(first='Justin', last='Burmesch', utype='Admin', email='j@b.com',
             password='TestPass'),
        User(first='Test', last='Teacher', utype='Teacher', email='t@t.com',
             password='TestPass'),
        User(first='Test', last='Student', utype='Student', email='t@s.com',
             password='TestPass')
    ]
    return users


def create_teacher():
    teacher = Teacher(user_id=2)
    return teacher


def create_schedule():
    schedule = Schedule(teacher_id=1,
                        date_time=datetime.datetime(2020, 6, 20, 13, 00),
                        meeting_id=1)
    return schedule


def create_zoom():
    zoom = Zoom(account='zoom@account.com')
    return zoom


def create_meeting():
    meeting = Meeting(student_id=3)
    return meeting


main()
