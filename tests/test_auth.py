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
        self.pr('Main', response)

    def test_register(self):
        course1 = Course(name='ADMIN', code='ADMIN')
        course2 = Course(name='TEST', code='TEST')
        db.session.add(course1)
        db.session.add(course2)
        db.session.commit()

        response = self.register_admin()
        self.assertEqual(response.status_code, 200)
        self.pr('Reg Admin', response)

        response = self.register_student()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account Created. Please check your '
                      + b'email for account validation.', response.data)
        self.pr('Reg Student', response)

        # nopass = dict(
        #     code='TEST',
        #     first='Test',
        #     last='Student',
        #     email='test@student.com',
        #     password=None,
        #     confirm_password=None
        # )


if __name__ == "__main__":
    unittest.main()
