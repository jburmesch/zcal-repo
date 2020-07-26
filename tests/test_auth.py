import unittest
from flask_testing import TestCase
from zcal import create_app as create, db
from zcal.models import (
    Course  # , User, Teacher, Schedule, Meeting, Student, Zoom, Timeslot
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

    '''Helper Methods'''
    def login(self, email, password):
        return self.client.post('/auth/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.get('/logout', follow_redirects=True)

    def register(self, code, first, last, email, password,
                 confirm_password):
        return self.client.post('/auth/register', data=dict(
            code=code,
            first=first,
            last=last,
            email=email,
            password=password,
            confirm_password=confirm_password
        ), follow_redirects=True)

    def register_admin(self):
        return self.register(
            code='ADMIN',
            first='Test',
            last='Admin',
            email='test@admin.com',
            password='testpass',
            confirm_password='testpass'
        )

    def login_admin(self):
        return self.login(
            email='test@admin.com',
            password='testpass'
        )

    def register_student(self):
        return self.register(
            code='TEST',
            first='Test',
            last='Student',
            email='test@student.com',
            password='testpass',
            confirm_password='testpass'
        )

    def login_student(self):
        return self.login(
            email='test@student.com',
            password='testpass'
        )

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

        # ensure that the first user can register using the admin course
        response = self.register_admin()
        self.assertEqual(response.status_code, 200)

        # ensure that a student can register successfuly
        response = self.register_student()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Created. Please check your '
                      + b'email for account validation.', response.data)

        # test non-matching passwords
        response = self.register(
            code='TEST',
            first='Test',
            last='Student',
            email='test@student.com',
            password="testpass",
            confirm_password="t"
        )
        self.assertIn(b'Field must be equal to password.', response.data)

        # test bad email address
        response = self.register(
            code='TEST',
            first='Test',
            last='Student',
            email='t',
            password="testpass",
            confirm_password="testpass"
        )
        self.assertIn(b'Invalid email address.', response.data)

        # test non-existant course code
        response = self.register(
            code='x',
            first='Test',
            last='Student',
            email='t',
            password="testpass",
            confirm_password="testpass"
        )
        self.assertIn(b'Course code not found.', response.data)

        # make sure that admin registration doesn't work after 
        # first user is registered
        response = self.register(
            code='ADMIN',
            first='Test',
            last='Student',
            email='t@s.com',
            password="testpass",
            confirm_password="testpass"
        )
        self.assertIn(b'Course code not found.', response.data)

        # test passwords that are too short
        response = self.register(
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


if __name__ == "__main__":
    unittest.main()
