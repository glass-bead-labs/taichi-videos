import logging
from datetime import date
import csv

import morepath
from more import static
from morepath.security import Identity, NO_IDENTITY

from .static import all_components

## Set up our App

# class App(morepath.App):
class App(static.StaticApp):
    pass

@App.static_components()
def get_static_components():
        return all_components

## Site root

@App.path(path='')
class Root(object):
    pass

@App.html(model=Root)
def hello_word(self, request):
    request.include('bootstrap')
    request.include('taichi_style')

    with open('resources/index.html', 'r') as file_obj:
        result = file_obj.read()
    # with open('log.csv', 'a') as log:
    #     log.write('I got a request at {}\n'.format(date.today()))
    logging.info('I got a request at {}\n'.format(date.today()))
    return result

@App.path(path='login')
class Login(object):
    def __init__(self):
        with open('resources/example-passwords.csv') as csvfile:
            records = csv.reader(csvfile)
            self.passwords = {rec[0]: rec[1] for rec in records}

@App.html(model=Login)
def login_form(self, request):
    request.include('bootstrap')
    with open('resources/login.html', 'r') as file_obj:
        result = file_obj.read()

    return result

@App.html(model=Login, request_method='POST')
def login_validate(self, request):
    # Replace this function body with looking up in self.passwords and activate
    # morepath "logged in" machinery:
    # http://morepath.readthedocs.org/en/latest/security.html#login-and-logout
    def user_has_password(usrnm, pwd):
        return usrnm in self.passwords.keys() and pwd in self.passwords.values()
    p = request.POST
    username = p['username']
    password = p['password']
    if not user_has_password(username, password):
        return 'Sorry, invalid username/password combination'

    @request.after
    def remember(response):
        identity = morepath.Identity(username)
        morepath.remember_identity(response, request, identity)
    #return 'You typed {}, {}'.format(p['username'], p['password'])

# @App.identity_policy()
# def get_identity_policy():
#     return BasicAuthIdentityPolicy()

# @App.verify_identity()
# def verify_identity(identity):
#     return user_has_password(identity.username, identity.password)

def main():
    config=morepath.setup()
    config.scan()
    config.scan(static)
    config.commit()
    wsgi = App()
    morepath.run(wsgi)
