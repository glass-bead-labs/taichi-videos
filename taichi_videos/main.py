import logging
from datetime import date
import csv

import morepath
from more import static
from morepath.security import Identity, NO_IDENTITY
from more.itsdangerous import IdentityPolicy

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

    # No idea why I was having trouble with this earlier
    logging.info('I got a request at {}'.format(date.today()))
    return result

@App.path(path='login')
class Login(object):
    '''Simple class that has keeps all passwords in memory'''
    def __init__(self):
        with open('resources/example-passwords.csv') as csvfile:
            records = csv.reader(csvfile)
            self.passwords = {rec[0]: rec[1] for rec in records}

    def user_has_password(self, usrnm, password):
        '''Look up the password for usrnm and make sure it matches'''
        try:
            return self.passwords[usrnm] == password
        except KeyError:
            return False

@App.html(model=Login)
def login_form(self, request):
    request.include('bootstrap')
    with open('resources/login.html', 'r') as file_obj:
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

@App.identity_policy()
def get_identity_policy():
    return IdentityPolicy()

@App.verify_identity()
def verify_identity(identity):
    # We don't care who they are for verification
    # If we get this far, it means we've assigned a valid identity
    return True

def main():
    logging.basicConfig(filename='log/events.csv',level=logging.INFO)

    config=morepath.setup()
    config.scan()
    config.scan(static)
    config.commit()
    wsgi = App()
    morepath.run(wsgi)
