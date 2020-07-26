from flask_testing import TestCase
from zcal import create_app as create, db
from zcal.models import (
    Course  # , User, Teacher, Schedule, Meeting, Student, Zoom, Timeslot
)
from tests.helpers import (
    register, register_admin, register_student, login,
    login_admin, login_student
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
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        # need courses for users to be created successfuly
        course1 = Course(name='ADMIN', code='ADMIN')
        course2 = Course(name='TEST', code='TEST')
        db.session.add(course1)
        db.session.add(course2)
        db.session.commit()

        # check that first user admin registration works.
        response = register_admin(self)
        self.assertEqual(response.status_code, 200)

        # check that student registration works.
        response = register_student(self)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Created. Please check your '
                      + b'email for account validation.', response.data)

        # check that mismatched passwords don't work.
        response = register(
            test=self,
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
            test=self,
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
            test=self,
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
            test=self,
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
            test=self,
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
        course1 = Course(name='ADMIN', code='ADMIN')
        course2 = Course(name='TEST', code='TEST')
        db.session.add(course1)
        db.session.add(course2)
        db.session.commit()
        response = register_admin(self)

        # check that admin can log in
        response = login_admin(self)
        self.assert200(response)
        self.assertIn(
            b'Manage Teachers',
            response.data
        )

        # check that student can log in
        response = login_student(self)
        self.assert200(response)
        self.assertIn(
            b'Mon',
            response.data
        )

        response = register_student(self)
