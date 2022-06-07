from email import message
from django import urls
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User

from django.dispatch import receiver

from student.models import Student

import pytest


@pytest.fixture
def user_data():
    return {'username': 'User1', 'email': 'User1@gmail.com', 'password1': 'qwerty3211', 'password2': 'qwerty3211'}


@pytest.fixture
def user_data_2():
    return {'username': 'User2', 'email': 'User2@gmail.com', 'password1': 'qwerty3211', 'password2': 'qwerty3211'}


@pytest.fixture
def login_user_data():
    return {'username': 'User1', 'password': 'qwerty3211'}


@pytest.fixture
def delete_user_data():
    return {'username': 'User1'}


# Testing views rendering
@pytest.mark.parametrize('param', [
    ('login'),
    ('register'),
])
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


# Testing unauthoeize user access. 302 because autenfication required
@pytest.mark.parametrize('param', [
    ('chats')
])
def test_render_views_unauthorized_user(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 302


# (registration user) Testing user registration using 'register' url
@pytest.mark.django_db
def test_usesr_signup(client, user_data):
    user_model = get_user_model()

    assert user_model.objects.count() == 0

    singup_url = urls.reverse('register')

    resp = client.post(singup_url, user_data)

    assert user_model.objects.count() == 1
    assert resp.status_code == 302


# (login user) Testing user registration and login using 'register' url and 'login' url
@pytest.mark.django_db
def test_usesr_signup_and_login(client, user_data, login_user_data):
    user_model = get_user_model()

    assert user_model.objects.count() == 0

    singup_url = urls.reverse('register')

    resp = client.post(singup_url, user_data)

    assert user_model.objects.count() == 1
    assert resp.status_code == 302

    login_url = urls.reverse('login')
    resp = client.post(login_url, login_user_data)
    assert user_model.is_authenticated


# (deleting user) Testing user registration and login and user_acc deleting using 'register' url and 'login' url and 'delete' url
@pytest.mark.django_db
def test_usesr_signup_and_login_and_deleting(client, user_data, login_user_data, delete_user_data):
    user_model = get_user_model()

    assert user_model.objects.count() == 0

    singup_url = urls.reverse('register')

    resp = client.post(singup_url, user_data)

    assert user_model.objects.count() == 1
    assert resp.status_code == 302

    login_url = urls.reverse('login')
    resp = client.post(singup_url, login_user_data)
    assert user_model.is_authenticated

    delete_url = urls.reverse('delete')

    user_model.objects.filter(username=delete_user_data['username']).delete()

    assert user_model.is_authenticated

    assert user_model.objects.count() == 0


# Testing user searching
@pytest.mark.django_db
def test_user_searching(client, user_data, user_data_2, login_user_data):
    user_model = get_user_model()

    singup_url = urls.reverse('register')

    client.post(singup_url, user_data)

    client.post(singup_url, user_data_2)

    assert user_model.objects.count() == 2

    login_url = urls.reverse('login')
    resp = client.post(login_url, login_user_data)
    assert user_model.is_authenticated

    resp = client.get('/search/User2/')

    assert not resp == None


# Testing user messaging
@pytest.mark.django_db
def test_user_messaging(client, user_data, user_data_2, login_user_data):
    user_model = get_user_model()

    singup_url = urls.reverse('register')

    client.post(singup_url, user_data)

    client.post(singup_url, user_data_2)

    assert user_model.objects.count() == 2

    login_url = urls.reverse('login')
    client.post(login_url, login_user_data)
    assert user_model.is_authenticated

    assert Student.objects.count() == 0

    u1 = User()
    u2 = User()


u1.username = "User3"
u1.save()
u2.username = "User4"
u2.save()

msg = Student()

msg.sender = u1
msg.receiver = u2
msg.message = "HELLO"
msg.save()

assert Message.objects.count() == 1