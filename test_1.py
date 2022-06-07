from django import urls
from django.contrib.auth import get_user_model

import pytest


@pytest.fixture
def user_t():
    return {'username': 'Goga',
            'password': '1234',
            'firstname': 'Gog',
            'lastname': 'Zept',
            'mobile':'+375296451428',
            'address':'goga@gmail.com'}


@pytest.fixture
def user_d():
    return {'username': 'Rapicas',
            'password': '1111',
            'firstname': 'Dima',
            'lastname': 'Petrynko',
            'mobile': '+375294518632',
            'address': 'dimatopchik@gmail.com'}


@pytest.fixture
def login_user_data():
    return {'username': 'Goga',
            'password': '1234'}


# Testing views rendering
@pytest.mark.parametrize('param', [
    ('studentlogin'),
    ('studentsignup'),
])
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


# Testing unauthoeize user access. 302 because autenfication required
@pytest.mark.parametrize('param', [
    ('students')
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

    singup_url = urls.reverse('studentsignup')

    resp = client.post(singup_url, user_data)

    assert user_model.objects.count() == 1
    assert resp.status_code == 302


# (login user) Testing user registration and login using 'register' url and 'login' url
@pytest.mark.django_db
def test_usesr_signup_and_login(client, user_data, login_user_data):
    user_model = get_user_model()

    assert user_model.objects.count() == 0

    singup_url = urls.reverse('studentsignup')

    resp = client.post(singup_url, user_data)

    assert user_model.objects.count() == 1
    assert resp.status_code == 302

    login_url = urls.reverse('studentlogin')
    resp = client.post(login_url, login_user_data)
    assert user_model.is_authenticated


#Testing user registration and login
@pytest.mark.django_db
def test_usesr_signup_and_login_and_deleting(client, user_data, login_user_data, delete_user_data):
    user_model = get_user_model()

    assert user_model.objects.count() == 0

    singup_url = urls.reverse('studentsignup')

    resp = client.post(singup_url, user_data)

    assert user_model.objects.count() == 1
    assert resp.status_code == 302

    login_url = urls.reverse('studentlogin')
    resp = client.post(singup_url, login_user_data)
    assert user_model.is_authenticated

    assert user_model.objects.count() == 0


# Testing student
@pytest.mark.django_db
def test_user_searching(client, user_data, user_data_2, login_user_data):
    user_model = get_user_model()

    singup_url = urls.reverse('studentsignup')

    client.post(singup_url, user_data)

    client.post(singup_url, user_data_2)

    assert user_model.objects.count() == 2

    login_url = urls.reverse('studentlogin')
    resp = client.post(login_url, login_user_data)
    assert user_model.is_authenticated

    resp = client.get('/search/User2/')

    assert not resp == None