from flask_testing import TestCase
from zcal import create_app as create, db
import tests.helpers as h
from flask import url_for
from zcal.models import Teacher, Course
import random
from datetime import datetime


class AuthTest(TestCase):

    def create_app(self):
        app = create(True)
        return app

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    '''Tests'''
    def test_add_teacher(self):
        c = self.client
        with c:
            h.create_courses()
            h.register_admin(c)
            h.login_admin(c)

            # make sure page is accessible
            response = c.get(url_for('admin.add_teacher'))
            self.assert_200(response)

            # check that teacher creation works
            response = c.post(
                url_for('admin.add_teacher'), data=dict(
                    first='Test',
                    last='Teacher',
                    email='test@teacher.com'
                ), follow_redirects=True
            )
            self.assertIn(b'Account Created.', response.data)
            h.logout(c)

        with c:
            h.register_admin(c)
            h.login_admin(c)

            # check that bad email doesn't work
            response = c.post(
                url_for('admin.add_teacher'), data=dict(
                    first='Test',
                    last='Teacher',
                    email='x'
                ), follow_redirects=True
            )
            self.assertIn(b'Invalid email address.', response.data)
            h.logout(c)

        with c:
            h.register_admin(c)
            h.login_admin(c)

            # log in 10 teachers
            h.reg_10_teachers(self)
            h.logout(c)

    def test_manage_teachers(self):
        c = self.client
        h.create_courses()

        with c:
            h.register_admin(c)
            h.login_admin(c)
            h.reg_10_teachers(self)
            teachers = Teacher.query.all()
            count = 0
            # check that all teachers redirect correctly for 'manage'
            for teacher in teachers:
                count += 1
                response = c.post(
                    url_for('admin.teachers'), data=dict(
                        mg_id=teacher.id
                    )
                )
                self.assertRedirects(response, url_for(
                    'cal.cal',
                    u_id=teacher.user_id
                ))
            # check that 11 doesn't redirect
            response = c.post(
                url_for('admin.teachers', data=dict(
                    mg_id=11
                ))
            )
            self.assert200(response)

            # remove all teachers in random order
            m = len(teachers) - 1
            order = []
            for n in range(m):
                i = random.randint(1, m )
                order.append(i)
                response = h.remove_teacher(c, teachers[i].id)
                teachers = Teacher.query.all()
                m -= 1
                self.assertIn(
                    b'Teacher successfully removed.',
                    response.data,
                    f'\n\nFailed To Remove Teacher - Removal Order: {order}'
                )
            # make sure that all 10 teachers have been removed
            assert len(teachers) == 1
            # register teacher with zoom account
            t = h.make_teacher()
            z = h.make_zoom()
            t.zoom_id = z.id
            db.session.commit()
            # make sure the teacher has been removed
            response = h.remove_teacher(c, t.id)
            self.assertIn(
                    b'Teacher successfully removed.',
                    response.data
                )
            # Add another teacher and student
            h.make_course()
            s = h.make_student()
            t = h.make_teacher()
            # schedule a meeting between them
            sched = h.make_schedule(t.id, s.id, datetime.now().time(), 45)
            assert sched.meeting.student == s
            response = h.remove_teacher(c, t.id)
            self.assertIn(
                    b'Teacher has meetings scheduled!'
                    + b' Reschedule before removing!',
                    response.data
                )

    def test_add_course(self):
        c = self.client
        h.create_courses()

        with c:
            h.register_admin(c)
            h.login_admin(c)

            # create 10 courses, and make sure that they show up.
            for i in range(10):
                count = i + 1
                response = h.register_course(
                    client=c,
                    name=f'Course {count}',
                    code=f'C{count}'
                )
                self.assertRedirects(response, url_for('admin.add_course'))
                response = c.get(url_for('admin.courses'))
                c_name = f'Course {count}'
                self.assertIn(bytes(c_name, 'utf-8'), response.data)

    def test_manage_courses(self):
        c = self.client
        h.create_courses()

        with c:
            h.register_admin(c)
            h.login_admin(c)

            for i in range(10):
                count = i + 1
                h.register_course(
                    client=c,
                    name=f'Course {count}',
                    code=f'C{count}'
                )

            for i in range(10):
                response = c.post(
                    url_for('admin.courses'),
                    data=dict(
                        mg_id=i+3
                    )
                )
                self.assertIn(b': Students', response.data)

            courses = Course.query.all()
            # remove all courses in random order
            m = len(courses)
            order = []
            for n in range(m - 2):
                i = random.randint(2, m - 1)
                order.append(i)
                response = h.remove_course(c, courses[i].id)
                courses = Course.query.all()
                m -= 1
                self.assertIn(
                    b'Course Deleted.',
                    response.data,
                    f'\n\nFailed To Remove Teacher - Removal Order: {order}'
                )

            # create another course and add a student to it.
            course = h.register_course(
                client=c,
                name='Course A',
                code='CA'
            )
            course = Course.query.filter(Course.code == 'CA').first()
            h.make_student(c_id=course.id)
            response = h.remove_course(c, course.id)
            # make sure that removing it is not successful.
            self.assertIn(
                b'This course can not be removed while it'
                + b' has students attached to it.', response.data
            )
