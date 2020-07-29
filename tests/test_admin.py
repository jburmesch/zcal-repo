from flask_testing import TestCase
from zcal import create_app as create, db
from tests.helpers import (
    register_admin, register_student, login_admin, login_student, logout,
    create_courses, register_teacher, login_teacher
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
    def test_add_Teacher(self):
        c = self.client
        with c:
            create_courses()
            register_admin()
            login_admin()

            response=c.get(url_for('admin.add_teacher'))
            assert_200(response)

            response=c.post(url_for('admin.add_teacher',))
