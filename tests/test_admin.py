from flask_testing import TestCase
from zcal import create_app as create, db
import tests.helpers as h
from flask import url_for
from zcal.models import Teacher
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
            m = 10
            order = []
            for n in range(m):
                i = random.randint(0, m - 1)
                order.append(i)
                response = c.post(
                    url_for('admin.teachers'), data=dict(
                        rem_id=teachers[i].id
                    ), follow_redirects=True
                )
                teachers = Teacher.query.all()
                m -= 1
                self.assertIn(
                    b'Teacher successfully removed.',
                    response.data,
                    f'\n\nFailed To Remove Teacher - Removal Order: {order}'
                )
            # make sure that all 10 teachers have been removed
            assert len(teachers) == 0
            # register teacher with zoom account
            t = h.make_teacher()
            z = h.make_zoom()
            t.zoom_id = z.id
            db.session.commit()
            # make sure the teacher has been removed
            response = c.post(
                url_for('admin.teachers'), data=dict(
                    rem_id=t.id
                ), follow_redirects=True
            )
            self.assertIn(
                    b'Teacher successfully removed.',
                    response.data
                )
            # Add another teacher and student
            c = h.make_course()
            s = h.make_student()
            t = h.make_teacher()
            # schedule a meeting between them
            sched = h.make_schedule(t.id, s.id, datetime.now().time(), 45)
            print(sched)
