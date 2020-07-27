from zcal import db
from zcal.models import Course


def create_courses():
    course1 = Course(name='ADMIN', code='ADMIN')
    course2 = Course(name='TEST', code='TEST')
    db.session.add(course1)
    db.session.add(course2)
    db.session.commit()


def pr(title, response):
    print(f'\n{title}: \n{str(response)}')


def login(client, email, password):
    return client.post('/auth/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/auth/logout', follow_redirects=True)


def register(client, code, first, last, email, password,
             confirm_password):
    return client.post('/auth/register', data=dict(
        code=code,
        first=first,
        last=last,
        email=email,
        password=password,
        confirm_password=confirm_password
    ), follow_redirects=True)


def register_admin(client):
    return register(
        client=client,
        code='ADMIN',
        first='Test',
        last='Admin',
        email='test@admin.com',
        password='testpass',
        confirm_password='testpass'
    )


def login_admin(client):
    return login(
        client=client,
        email='test@admin.com',
        password='testpass'
    )


def register_student(client):
    return register(
        client=client,
        code='TEST',
        first='Test',
        last='Student',
        email='test@student.com',
        password='testpass',
        confirm_password='testpass'
    )


def login_student(client):
    return login(
        client=client,
        email='test@student.com',
        password='testpass'
    )
