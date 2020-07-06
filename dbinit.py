from zcal import create_app, db
from zcal.models import (
    Course, User, Teacher, Student, Schedule, Zoom, Meeting, Timeslot
)
import datetime

app = create_app()
app.app_context().push()


def main():
    answer = input("RUNNING THIS WILL **DROP** ANY EXISTING DB TABLES! "
                   + "Are you sure?")
    if answer == 'y':
        db.drop_all()
        db.create_all()

        course = create_course()
        users = create_users()
        teachers = create_teachers()
        students = create_students()
        schedules = create_schedules()
        zooms = create_zooms()
        meetings = create_meetings()
        timeslots = create_timeslots()

        db.session.add(course)

        db.session.commit()
        print(Course.query.all())

        for user in users:
            db.session.add(user)
        db.session.commit()
        print(User.query.all())

        for student in students:
            db.session.add(student)
        db.session.commit()
        print(Student.query.all())

        for teacher in teachers:
            db.session.add(teacher)
        db.session.commit()

        for meeting in meetings:
            db.session.add(meeting)
        db.session.commit()

        for schedule in schedules:
            db.session.add(schedule)
        db.session.commit()

        for slot in timeslots:
            db.session.add(slot)
        db.session.commit

        print(Meeting.query.all())
        print(Schedule.query.all())

        for zoom in zooms:
            db.session.add(zoom)
        db.session.commit()

        print(Zoom.query.all())
        print(Teacher.query.all())
        print(Timeslot.query.all())

        db.drop_all()
        db.create_all()
        course = create_course()

        db.session.add(course)
        db.session.commit()

        print('\n')
        print('Database has been reinitialized.'
              + 'The next user to register will be admin!')
        print(Course.query.all())

    else:
        print('Whew. Crisis averted.')


def create_course():
    course = Course(
        name='ADMIN',
        code='ADMIN'
    )
    return course


def create_users():
    users = [
        User(first='Admin', last='Istrator', utype='Admin', email='admin',
             password='adminpass'),
        User(first='Test', last='Teacher', utype='Teacher', email='t@t.com',
             password='TestPass'),
        User(first='Test', last='Student', utype='Student', email='t@s1.com',
             password='TestPass'),
        User(first='Test', last='Student2', utype='Student', email='t@s2.com',
             password='TestPass'),
        User(first='Test', last='Student3', utype='Student', email='t@s3.com',
             password='TestPass'),
        User(first='Test', last='Teacher2', utype='Student', email='t@t2.com',
             password='TestPass'),
        User(first='Test', last='Teacher3', utype='Student', email='t@t3.com',
             password='TestPass')
    ]
    return users


def create_students():
    students = [
        Student(user_id=3, course_id=1),
        Student(user_id=4, course_id=1),
        Student(user_id=5, course_id=1)
    ]
    return students


def create_teachers():
    teacher = [
        Teacher(user_id=2, zoom_id=1),
        Teacher(user_id=6, zoom_id=2),
        Teacher(user_id=7, zoom_id=3)
    ]
    return teacher


def create_schedules():
    schedules = [
        Schedule(
            teacher_id=1,
            date=datetime.date(2020, 6, 27),
            start=datetime.time(8, 00),
            end=datetime.time(8, 45),
            duration=45,
            meeting_id=1
        ),
        Schedule(
            teacher_id=1,
            date=datetime.date(2020, 6, 27),
            start=datetime.time(9, 00),
            end=datetime.time(9, 45),
            duration=45
        ),
        Schedule(
            teacher_id=2,
            date=datetime.date(2020, 6, 27),
            start=datetime.time(8, 00),
            end=datetime.time(8, 45),
            duration=45,
            meeting_id=2
        ),
        Schedule(
            teacher_id=3,
            date=datetime.date(2020, 6, 27),
            start=datetime.time(8, 00),
            end=datetime.time(8, 45),
            duration=45,
            meeting_id=3
        ),
        Schedule(
            teacher_id=3,
            date=datetime.date(2020, 6, 27),
            start=datetime.time(9, 00),
            end=datetime.time(9, 45),
            duration=45
        )
    ]

    return schedules


def create_zooms():
    zooms = [
        Zoom(
            account="account1@zoom.com",
            zoom_account_id='abcdefghijklmnopqrstuvwxyz',
            refresh='sda;flkjhew083h20fisdh08823y04uhfg0ewyh408hf'
        ),
        Zoom(
            account="account2@zoom.com",
            zoom_account_id='sdlkfhweournsdlkvhowo',
            refresh='dslfhw39ouvbdlfivh2o834hfv97sdheef09fo8h230'
        ),
        Zoom(
            account="account3@zoom.com",
            zoom_account_id='sldkfhwoeunvuo9sghviwue',
            refresh='hsdoufebwovclskjdehygoeughfoshf03128yt4923uhgtf9s7dyt3'
        )
    ]
    return zooms


def create_meetings():
    meetings = [
        Meeting(student_id=1),
        Meeting(student_id=2),
        Meeting(student_id=3)
    ]
    return meetings


def create_timeslots():
    timeslots = [
        Timeslot(
            created_by=1,
            start=datetime.time(14, 0),
            duration=60,
            end=datetime.time(15, 0)
        ),
        Timeslot(
            created_by=1,
            start=datetime.time(15, 0),
            duration=60,
            end=datetime.time(16, 0)
        ),
        Timeslot(
            created_by=1,
            start=datetime.time(16, 0),
            duration=60,
            end=datetime.time(17, 0)
        ),
        Timeslot(
            created_by=1,
            start=datetime.time(17, 0),
            duration=60,
            end=datetime.time(18, 0)
        ),
    ]
    return timeslots


main()
