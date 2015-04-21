import csv

import morepath
# from morepath.security import Identity, NO_IDENTITY
# from more.itsdangerous import IdentityPolicy
from webob.exc import HTTPForbidden

from .app import App

# The lone availible permission


class ViewPermission:
    pass


# We have a uniform permission rule for ViewPermission
@App.permission_rule(model=object, permission=ViewPermission)
def generic_view_permission(identity, model, permission):
    return True


# @App.permission_rule(model=object, permission=ViewPermission, identity=None)
# def has_permission_not_logged_in(identity, model, permission):
#     return True
#

# @App.identity_policy()
# def get_identity_policy():
#     return IdentityPolicy()


@App.verify_identity()
def verify_identity(identity):
    # By default, morepath rejects all identities.  We are using cookies that
    # should ensure identities are valid, so we don't care who they are for
    # verification.  If we get this far, it means we've assigned a valid
    # identity.
    return True


@App.view(model=HTTPForbidden)
def redirect_to_login(self, request):
    # More clever would be to remember the URL we came from as a '?' expression
    return morepath.redirect(request.link(login))


# Login interface


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
    request.include('taichi_style')
    with open('resources/login.html', 'r') as file_obj:
        result = file_obj.read()

    return result


@App.view(model=Login, request_method='POST')
def login_validate(self, request):
    username = request.POST['username']
    password = request.POST['password']
    if not self.user_has_password(username, password):
        # Password is invalid
        # return 'Sorry, invalid username/password combination'
        return morepath.redirect(request.link(login))

    # @request.after
    # def remember(response):
    #     identity = morepath.Identity(username)
    #     morepath.remember_identity(response, request, identity)
    response = morepath.redirect('/video/14')
    identity = morepath.Identity(username)
    morepath.remember_identity(response, request, identity)

    return response

    # return morepath.redirect('/video/14')
    # return 'Logged in {}'.format(username)

# @App.path(path='signup')
# class Signup(object):
#     pass


# @App.html(model=Signup)
# def signup_form(self, request):
#     request.include('bootstrap')
#     with open('resources/signup.html', 'r') as file_obj:
#         result = file_obj.read()
#     return result
