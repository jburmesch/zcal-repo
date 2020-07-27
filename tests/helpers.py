

def pr(title, response):
    print(f'\n{title}: \n{str(response)}')


def login(test, email, password):
    return test.client.post('/auth/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(test):
    return test.client.get('/auth/logout', follow_redirects=True)


def register(test, code, first, last, email, password,
             confirm_password):
    return test.client.post('/auth/register', data=dict(
        code=code,
        first=first,
        last=last,
        email=email,
        password=password,
        confirm_password=confirm_password
    ), follow_redirects=True)


def register_admin(test):
    return register(
        test=test,
        code='ADMIN',
        first='Test',
        last='Admin',
        email='test@admin.com',
        password='testpass',
        confirm_password='testpass'
    )


def login_admin(test):
    return login(
        test=test,
        email='test@admin.com',
        password='testpass'
    )


def register_student(test):
    return register(
        test=test,
        code='TEST',
        first='Test',
        last='Student',
        email='test@student.com',
        password='testpass',
        confirm_password='testpass'
    )


def login_student(test):
    return login(
        test=test,
        email='test@student.com',
        password='testpass'
    )
