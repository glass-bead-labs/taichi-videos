import logging
from datetime import date
import csv

import morepath
# from morepath.security import Identity, NO_IDENTITY
from more.itsdangerous import IdentityPolicy
from webob.exc import HTTPForbidden

from .app import App
# Only for side-effects (noqa disables linter warning)
from . import static  # noqa

# Security stuff


class ViewPermission(object):
    pass


@App.identity_policy()
def get_identity_policy():
    return IdentityPolicy()


@App.verify_identity()
def verify_identity(identity):
    # We don't care who they are for verification
    # If we get this far, it means we've assigned a valid identity
    return True


@App.view(model=HTTPForbidden)
def redirect_to_login(self, request):
    return morepath.redirect(request.link(login))


# Site root


@App.path(path='')
class Root(object):
    pass


@App.html(model=Root, permission=ViewPermission)
def hello_word(self, request):
    # if not logged in, want to:
    request.include('bootstrap')
    request.include('taichi_style')

    with open('resources/index.html', 'r') as file_obj:
        result = file_obj.read()

    # No idea why I was having trouble with this earlier
    logging.info('I got a request at {}'.format(date.today()))
    return result


class Login(object):

    '''Simple class that keeps all passwords in memory'''

    def __init__(self, fname):
        with open(fname) as csvfile:
            records = csv.reader(csvfile)
            self.passwords = {rec[0]: rec[1] for rec in records}

    def user_has_password(self, usrnm, password):
        '''Look up the password for usrnm and make sure it matches'''
        try:
            return self.passwords[usrnm] == password
        except KeyError:
            return False

# We instantiate this object so we can redirect to it easily
login = Login('resources/example-passwords.csv')


@App.path(model=Login, path='login')
def get_login():
    # For now, we just return the instantiated Login object
    return login


@App.html(model=Login)
def login_form(self, request):
    request.include('bootstrap')
    with open('resources/login.html', 'r') as file_obj:
        result = file_obj.read()

    return result


@App.path(path='signup')
class Signup(object):
    pass


@App.html(model=Signup)
def signup_form(self, request):
    request.include('bootstrap')
    with open('resources/signup.html', 'r') as file_obj:
        result = file_obj.read()
    return result


@App.html(model=Login, request_method='POST')
def login_validate(self, request):
    username = request.POST['username']
    password = request.POST['password']
    if not self.user_has_password(username, password):
        return 'Sorry, invalid username/password combination'

    @request.after
    def remember(response):
        identity = morepath.Identity(username)
        morepath.remember_identity(response, request, identity)

    return 'You typed {}, {}'.format(username, password)


def main():
    logging.basicConfig(filename='log/events.csv', level=logging.INFO)

    # Now configuring to use autosetup
    # config=morepath.setup()
    # config.scan()
    # config.scan(static)
    # config.commit()
    morepath.autosetup()
    wsgi = App()
    morepath.run(wsgi)
