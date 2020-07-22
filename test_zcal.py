from flask.ext.testing import TestCase

from zcal import create_app, db, init_db


class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///testing/test.db"
    TESTING = True

    def create_app(self):

        # pass in test configuration
        return create_app(self)

    def setUp(self):

        init_db

    def tearDown(self):

        db.session.remove()
        db.drop_all()