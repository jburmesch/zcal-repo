from flask_testing import TestCase
from zcal import create_app as create, db
from tests.helpers import (
    register_admin, register_student, login_admin, login_student, logout,
    create_courses
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

    '''Tests'''
    # make sure that main is accessible
    def test_main(self):
        c = self.client
        create_courses()
        # test logged out users
        response = c.get("/", follow_redirects=True)
        self.assert200(response)
        self.assertIn(
            b'Not registered? <a href="/auth/register">Register here.</a>',
            response.data
        )

        # test admin
        with c:
            register_admin(c)
            login_admin(c)
            response = c.get("/", follow_redirects=True)
            self.assertIn(b'Manage Teachers', response.data)
            logout(c)

        # test students
        with c:
            register_student(c)
            login_student(c)
            response = c.get("/", follow_redirects=True)
            self.assertIn(b'Mon', response.data)
            logout(c)
