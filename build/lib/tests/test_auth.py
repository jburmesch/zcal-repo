from flask_testing import TestCase
from zcal import create_app as create, db
from tests.helpers import (
    register, register_admin, register_student, login,
    login_admin, login_student, logout, create_courses,
    make_teacher, login_teacher
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
    def test_register(self):
        # need courses for users to be created successfuly
        c = self.client
        create_courses()

        # check that first user admin registration works.
        response = register_admin(c)
        self.assertEqual(response.status_code, 200)

        # check that student registration works.
        response = register_student(c)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Created. Please check your '
                      + b'email for account validation.', response.data)

        # check that mismatched passwords don't work.
        response = register(
            client=c,
            code='TEST',
            first='Test',
            last='Student',
            email='test@student.com',
            password="testpass",
            confirm_password="t"
        )
        self.assertIn(b'Field must be equal to password.', response.data)

        # check that bad emails don't work
        response = register(
            client=c,
            code='TEST',
            first='Test',
            last='Student',
            email='t',
            password="testpass",
            confirm_password="testpass"
        )
        self.assertIn(b'Invalid email address.', response.data)

        # check that bad course codes don't work.
        response = register(
            client=c,
            code='x',
            first='Test',
            last='Student',
            email='t',
            password="testpass",
            confirm_password="testpass"
        )
        self.assertIn(b'Course code not found.', response.data)

        # check that admin login won't work after first user
        response = register(
            client=c,
            code='ADMIN',
            first='Test',
            last='Student',
            email='t@s.com',
            password="testpass",
            confirm_password="testpass"
        )
        self.assertIn(b'Course code not found.', response.data)

        # test passwords that are too short
        response = register(
            client=c,
            code='TEST',
            first='Test',
            last='Student',
            email='t@t.com',
            password="t",
            confirm_password="t"
        )
        self.assertIn(
            b'Field must be at least 8 characters long.',
            response.data
        )

    def test_login(self):
        # need courses for users to be created successfuly
        c = self.client
        create_courses()

        # check that admin can log in
        with c:
            register_admin(c)
            response = login_admin(c)
            self.assert200(response)
            self.assertIn(
                b'Manage Teachers',
                response.data
            )

            # logout admin
            response = logout(c)
            self.assertIn(
                b'Not registered? <a href="/auth/register">Register here.</a>',
                response.data
            )

        # check that student can log in
        with c:
            register_student(c)
            response = login_student(c)
            self.assertIn(
                b'Mon',
                response.data
            )
            # logout student
            response = logout(c)
            self.assertIn(
                b'Not registered? <a href="/auth/register">Register here.</a>',
                response.data
            )

        # check that bad email doesn't work
        response = login(
            client=c,
            email='x@x.com',
            password='testpass'
        )
        self.assertIn(
            b'Invalid email/password combination.',
            response.data
        )

        # check that bad password doesn't work
        response = login(
            client=c,
            email='test@student.com',
            password='x'
        )
        self.assertIn(
            b'Invalid email/password combination.',
            response.data
        )

        make_teacher()
        response = login_teacher(c)
        self.assertIn(
            b'Mon',
            response.data
        )
