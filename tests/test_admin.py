from flask_testing import TestCase
from zcal import create_app as create, db
from tests.helpers import (
    register_admin, login_admin, logout, create_courses,
    reg_10_teachers
)
from flask import url_for


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
            create_courses()
            register_admin(c)
            login_admin(c)

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
            logout(c)

        with c:
            register_admin(c)
            login_admin(c)

            # check that bad email doesn't work
            response = c.post(
                url_for('admin.add_teacher'), data=dict(
                    first='Test',
                    last='Teacher',
                    email='x'
                ), follow_redirects=True
            )
            self.assertIn(b'Invalid email address.', response.data)
            logout(c)

        with c:
            register_admin(c)
            login_admin(c)

            # log in 10 teachers
            reg_10_teachers(self)
            logout(c)

    def test_manage_teachers(self):
        c = self.client

        with c:
            register_admin(c)
            login_admin(c)
            reg_10_teachers(c)

