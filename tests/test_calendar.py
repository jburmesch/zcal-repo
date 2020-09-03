from flask_testing import TestCase
from zcal import create_app as create, db
from tests.helpers import (
    register_admin, register_student, login_admin, login_student, logout,
    create_courses, make_teacher, login_teacher
)
from flask import url_for
from flask_login import current_user


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
    # make sure that main is accessible
    def test_main(self):

        c = self.client
        create_courses()

        # test logged out users
        response = c.get(url_for('cal.main'))
        self.assertRedirects(response, url_for('auth.login'))

        # test admin
        with c:
            register_admin(c)
            login_admin(c)

            response = c.get(url_for('cal.main'))
            self.assertRedirects(
                response, url_for('admin.teachers')
            )
            logout(c)

        # test student
        with c:
            register_student(c)
            login_student(c)

            response = c.get(url_for('cal.main'))
            self.assertRedirects(
                response, url_for('cal.cal')
            )
            logout(c)

        # test teacher
        with c:
            make_teacher()
            login_teacher(c)

            response = c.get(url_for('cal.main'))
            self.assertRedirects(
                response, url_for('cal.cal')
            )
            logout(c)

    def test_cal(self):

        c = self.client
        create_courses()

        # test logged out
        response = c.get(url_for('cal.cal'))
        self.assertRedirects(response, url_for('auth.login', next='/calendar'))

        # test admin
        with c:

            register_admin(c)
            login_admin(c)

            # check redirect
            response = c.get(url_for('cal.cal'))
            self.assertRedirects(
                response, url_for(
                    'cal.t_cal',
                    u_id=current_user.id,
                    mod=0
                )
            )

            # make sure it loads
            response = c.get(url_for('cal.cal'), follow_redirects=True)
            self.assertIn(
                b'Mon', response.data
            )
            logout(c)

        # test student
        with c:

            register_student(c)
            login_student(c)

            # check redirect
            response = c.get(url_for('cal.cal'))
            self.assertRedirects(
                response, url_for(
                    'cal.stu_cal',
                    u_id=current_user.id,
                    mod=0
                )
            )

            # make sure it loads
            response = c.get(url_for('cal.cal'), follow_redirects=True)
            self.assertIn(
                b'Mon', response.data
            )
            logout(c)

        # test teacher
        with c:

            make_teacher()
            login_teacher(c)

            # check redirect
            response = c.get(url_for('cal.cal'))
            self.assertRedirects(
                response,
                url_for(
                    'cal.t_cal',
                    u_id=current_user.id,
                    mod=0
                )
            )

            # make sure it loads
            response = c.get(url_for('cal.cal'), follow_redirects=True)
            self.assertIn(
                b'Mon', response.data
            )
            logout(c)
