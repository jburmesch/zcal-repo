from zcal import db, bcrypt
from zcal.models import (
    Course, User, Teacher, Timeslot, Schedule, Meeting, Zoom, Student
)
from flask import url_for
from datetime import datetime, timedelta


def db_commit(entries):
    for entry in entries:
        db.session.add(entry)
    db.session.commit()


def create_courses():
    course1 = Course(name='ADMIN', code='ADMIN')
    course2 = Course(name='TEST', code='TEST')
    db_commit([course1, course2])


def pr(title, response):
    print(f'\n{title}: \n{str(response)}')


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


def login(client, email, password):
    return client.post('/auth/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/auth/logout', follow_redirects=True)


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


def register_course(client, name, code):
    return client.post(url_for('admin.add_course'), data=dict(
        name=name,
        code=code
    ))


def make_course():
    c = Course(
        name='Test Course',
        code='TC'
    )
    db_commit([c])
    return c


def make_student(c_id=None):
    if not c_id:
        c_id = make_course().id
    hashed_password = bcrypt.generate_password_hash(
        'testpass'
    ).decode('utf-8')

    u = User(
        first='Test',
        last='Student',
        utype='Student',
        email='test@student.com',
        password=hashed_password
    )
    db_commit([u])

    s = Student(
        user_id=u.id,
        course_id=c_id
    )
    db_commit([s])

    return(s)


def make_teacher():
    hashed_password = bcrypt.generate_password_hash(
        'testpass'
    ).decode('utf-8')

    user = User(
        first='Test',
        last='Teacher',
        utype='Teacher',
        email='test@teacher.com',
        password=hashed_password
    )
    db_commit([user])

    teacher = Teacher(
        user_id=user.id
    )
    db_commit([teacher])

    return teacher


def login_teacher(client):
    return login(
        client=client,
        email='test@teacher.com',
        password='testpass'
    )


def reg_10_teachers(test):
    for x in range(10):
        response = test.client.post(
            url_for('admin.add_teacher'), data=dict(
                first='Test',
                last='Teacher',
                email=f't{x}@t.com'
            ), follow_redirects=True
        )
        test.assertIn(b'Account Created.', response.data)


def create_timeslot(start, duration):
    end = (datetime(
                1, 1, 1, start.hour, start.minute
            ) + timedelta(minutes=45)).time()
    slot = Timeslot(
        created_by=1,
        start=start,
        end=end,
        duration=45
    )
    return slot


def make_schedule(t_id, s_id, start, duration):
    meeting = Meeting(student_id=s_id)
    ts = create_timeslot(start, duration)
    db_commit([meeting, ts])
    sched = Schedule(
        teacher_id=t_id,
        date=datetime.now().date(),
        start=start,
        end=ts.end,
        duration=duration,
        meeting_id=meeting.id
    )
    db_commit([sched])
    sched = Schedule.query.first()
    return sched


def make_zoom():
    z = Zoom(
        account='test@zoom.com',
        zoom_account_id='1234567',
        access='abc123',
        refresh='def456'
    )
    db_commit([z])
    return z


def remove_teacher(client, rem_id):
    return client.post(
        url_for('admin.teachers'), data=dict(
            rem_id=rem_id
        ), follow_redirects=True
    )


def remove_course(client, rem_id):
    return client.post(
        url_for('admin.courses'), data=dict(
            rem_id=rem_id
        ), follow_redirects=True
    )
