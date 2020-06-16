from zcal import db
from zcal.models import User, Teacher, Meeting, Schedule, Zoom, Course, Student
import datetime


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

        print(Meeting.query.all())
        print(Schedule.query.all())

        for zoom in zooms:
            db.session.add(zoom)
        db.session.commit()

        print(Zoom.query.all())
        print(Teacher.query.all())

        # db.drop_all()
        # db.create_all()
    else:
        print('Whew. Crisis averted.')


def create_course():
    course = Course(
        name='Test Co. Test Course',
        code='TCTC'
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
    student = [
        Student(user_id=3, course_id=1),
        Student(user_id=4, course_id=1),
        Student(user_id=5, course_id=1)
    ]
    return student


def create_teachers():
    teacher = [
        Teacher(user_id=2, zoom_id=1),
        Teacher(user_id=6, zoom_id=2),
        Teacher(user_id=7, zoom_id=3)
    ]
    return teacher


def create_schedules():
    schedules = [
        Schedule(teacher_id=1,
                 date_time=datetime.datetime(2020, 6, 20, 13, 00),
                 meeting_id=1),
        Schedule(teacher_id=1,
                 date_time=datetime.datetime(2020, 6, 21, 13, 00)),
        Schedule(teacher_id=2,
                 date_time=datetime.datetime(2020, 6, 22, 13, 00),
                 meeting_id=2),
        Schedule(teacher_id=3,
                 date_time=datetime.datetime(2020, 6, 23, 13, 00),
                 meeting_id=3),
        Schedule(teacher_id=3,
                 date_time=datetime.datetime(2020, 6, 24, 13, 00))
    ]

    return schedules


def create_zooms():
    zooms = [
        Zoom(account='zoom@account1.com'),
        Zoom(account='zoom@account2.com'),
        Zoom(account='zoom@account3.com')
    ]
    return zooms


def create_meetings():
    meetings = [
        Meeting(student_id=1),
        Meeting(student_id=2),
        Meeting(student_id=3)
    ]
    return meetings


main()
