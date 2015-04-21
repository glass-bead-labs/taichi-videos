'''Simply set up our App so it's importable'''

from more.static import StaticApp
from more.jinja2 import Jinja2App


class App(StaticApp, Jinja2App):
    pass


@App.template_directory()
def get_template_directory():
    return 'templates'
