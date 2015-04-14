import logging
from datetime import date
import csv
from csv import DictReader

import morepath
# from morepath.security import Identity, NO_IDENTITY
from more.itsdangerous import IdentityPolicy

from werkzeug.serving import run_simple

from .app import App
# Only for side-effects (noqa disables linter warning)
from . import static  # noqa

# Templating
#from more.jinja2 import Environment, PackageLoader, Jinja2App


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

@App.permission_rule(model=object, permission=ViewPermission, identity=None)
def has_permission_not_logged_in(identity, model, permission):
    return True

# Site root


@App.path(path='/')
class Root(object):
    pass


@App.html(model=Root, permission=ViewPermission)
def hello_word(self, request):
    # if not logged in, want to:
    # return morepath.redirect(request.link(login))
    request.include('bootstrap')
    request.include('taichi_style')

    with open('resources/index.html', 'r') as file_obj:
        result = file_obj.read()
        print(result)

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


@App.template_directory()
def get_template_directory():
    return 'templates'


def generate_template_key_value(src):
    with open(src) as csvfile:
        reader = csv.reader(csvfile)
        mydict = {row[0]: row[1] for row in reader}
    return mydict

# {
#     'title' : "Random Tai Chi Video",
#     'video14Description' : "This is a video of Taichi warmup",
#     'video14Src' : "//player.vimeo.com/video/119411037",
#     'video14Title' : "14-TAICHI-AT-HOME-PRACTICE-VIDEO"
# }
# env = Environment(loader=PackageLoader('taichi_videos', 'templates'))
# template = env.get_template('index.html')


@App.html(model=Login, request_method='POST', template="index.jinja2")
def login_validate(self, request):
    username = request.POST['username']
    password = request.POST['password']
    if not self.user_has_password(username, password):
        return 'Sorry, invalid username/password combination'

    @request.after
    def remember(response):
        identity = morepath.Identity(username)
        morepath.remember_identity(response, request, identity)

    request.include('bootstrap')
    request.include('taichi_style')

    with open('resources/all-videos.csv') as csvfile:
        reader = csv.reader(csvfile)
        myrow = [row for row in reader][1:]
    mydict = {
        'id': myrow[13][0],
        'title': myrow[13][1],
        'src': myrow[13][2],
        'desc': myrow[13][3]}
    # generate_template_key_value('resources/template-key-value.csv')
    template_values = mydict
    # with open('templates/index.html', 'r') as file_obj:
    #     result = file_obj.read()

    # No idea why I was having trouble with this earlier
    #logging.info('I got a request at {}'.format(date.today()))
    # template.render(template_values)
    return template_values

    # return
    #C[str(username)] = str(password)
    # return #'You typed {}, {}'.format(username, password)


class Video(object):

    def __init__(self, attribute_dict):
        self.attribute_dict = attribute_dict

with open('resources/all-videos.csv') as csvfile:
    reader = DictReader(csvfile)
    videos = {row['id']: Video(row) for row in reader}


@App.path(model=Video, path='/video/{vidId}')
def get_video(vidId):
    return videos[vidId]


@App.html(model=Video, template="index.jinja2")
def video(self, request):
    request.include('bootstrap')
    request.include('taichi_style')
    return self.attribute_dict


def main():
    # logging.basicConfig(filename='log/events.csv', level=logging.INFO)

    # Now configuring to use autosetup
    # config=morepath.setup()
    # config.scan()
    # config.scan(static)
    # config.commit()
    morepath.autosetup()
    wsgi = App()
    # morepath.run(wsgi)
    run_simple('localhost', 5000, wsgi, use_reloader=True)
