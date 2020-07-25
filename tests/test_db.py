import unittest
from flask_testing import TestCase
from zcal import create_app as create, db
import datetime
from zcal.models import (
    Course, User, Teacher, Schedule, Meeting, Student, Zoom, Timeslot
)


class AuthTest(TestCase):

    def create_app(self):
        app = create(True)
        return app

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    @staticmethod
    def pr(title, response):
        print(f'\n{title}: \n{str(response)}')

    '''Helper methods for DB testing'''
    @staticmethod
    def create_course():
        course = Course(
            name='ADMIN',
            code='ADMIN'
        )
        return course

    @staticmethod
    def create_users():
        users = [
            User(first='Admin', last='Istrator', utype='Admin',
                 email='admin', password='adminpass'),
            User(first='Test', last='Teacher', utype='Teacher',
                 email='t@t.com', password='TestPass'),
            User(first='Test', last='Student', utype='Student',
                 email='t@s1.com', password='TestPass'),
            User(first='Test', last='Student2', utype='Student',
                 email='t@s2.com', password='TestPass'),
            User(first='Test', last='Student3', utype='Student',
                 email='t@s3.com', password='TestPass'),
            User(first='Test', last='Teacher2', utype='Student',
                 email='t@t2.com', password='TestPass'),
            User(first='Test', last='Teacher3', utype='Student',
                 email='t@t3.com', password='TestPass')
        ]
        return users

    @staticmethod
    def create_students():
        students = [
            Student(user_id=3, course_id=1),
            Student(user_id=4, course_id=1),
            Student(user_id=5, course_id=1)
        ]
        return students

    @staticmethod
    def create_teachers():
        teacher = [
            Teacher(user_id=2, zoom_id=1),
            Teacher(user_id=6, zoom_id=2),
            Teacher(user_id=7, zoom_id=3)
        ]
        return teacher

    @staticmethod
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

    @staticmethod
    def create_zooms():
        zooms = [
            Zoom(
                account="account1@zoom.com",
                zoom_account_id='abcdefghijklmnopqrstuvwxyz',
                refresh='sda;flkjhew083h20fisdh08823y04uhfg0ewyh408hf',
                access='sdlkfhweljhsdflfhwe'
            ),
            Zoom(
                account="account2@zoom.com",
                zoom_account_id='sdlkfhweournsdlkvhowo',
                refresh='dslfhw39ouvbdlfivh2o834hfv97sdheef09fo8h230',
                access='sdlfkhwep;fuoihwefiugszdaliuga'
            ),
            Zoom(
                account="account3@zoom.com",
                zoom_account_id='sldkfhwoeunvuo9sghviwue',
                refresh='hsdoufebwovclskjdehygoeughfoshf03128yt4923uhgtf9s7',
                access='sdlfh2w9euhfowuhefpofihds00832hrfslkdyhoeyr'
            )
        ]
        return zooms

    @staticmethod
    def create_meetings():
        meetings = [
            Meeting(student_id=1),
            Meeting(student_id=2),
            Meeting(student_id=3)
        ]
        return meetings

    @staticmethod
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
    '''*********************'''
    '''Tests'''
    def test_db(self):

        course = self.create_course()
        users = self.create_users()
        teachers = self.create_teachers()
        students = self.create_students()
        schedules = self.create_schedules()
        zooms = self.create_zooms()
        meetings = self.create_meetings()
        timeslots = self.create_timeslots()

        db.session.add(course)
        db.session.commit()
        assert Course.query.first().name == 'ADMIN'

        for user in users:
            db.session.add(user)
        db.session.commit()
        users = User.query.all()
        for user in users:
            assert user.full_name()

        for student in students:
            db.session.add(student)
        db.session.commit()
        students = Student.query.all()
        for student in students:
            assert student.course.name == 'ADMIN'
            assert student.user.full_name()

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

        meetings = Meeting.query.all()
        for meeting in meetings:
            assert meeting.student.user.full_name()
            assert meeting.schedule.teacher.user.full_name()

        for zoom in zooms:
            db.session.add(zoom)
        db.session.commit()

        zooms = Zoom.query.all()
        for zoom in zooms:
            assert zoom.account

        teachers = Teacher.query.all()
        for teacher in teachers:
            assert teacher.user.full_name()

        timeslots = Timeslot.query.all()
        for timeslot in timeslots:
            assert Timeslot.start

        db.drop_all()
        db.create_all()

        # self.pr('DB Tests', 'Complete')


if __name__ == "__main__":
    unittest.main()
