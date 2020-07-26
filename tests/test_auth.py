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

        response = register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = register_student(self)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Created. Please check your '
                      + b'email for account validation.', response.data)

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
        pass
