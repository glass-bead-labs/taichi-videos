import os
from datetime import date

import morepath
from more import static
import bowerstatic

## Set up our App

# class App(morepath.App):
class App(static.StaticApp):
    pass

## Basic Bower stuff

bower = bowerstatic.Bower()
# Currently configured to look from directory where run
curr_dir = os.getcwd()
components = bower.components('app',
                              os.path.join(curr_dir, 'bower_components') )

### This stuff is just straight not working... :(

# # Local components must still have a bower.json
# local = bower.local_components('local', components)
# local.component(os.path.join(curr_dir, 'resources/taichi_style'),
#                 # Make the "version" change whenever code is changed
#                 # This should be changed for "production", but we're unlikely to
#                 # use this code in high-volume situations.
#                 version=None)

@App.static_components()
def get_static_components():
        return components

## Site root

@App.path(path='')
class Root(object):
    pass

@App.html(model=Root)
def hello_word(self, request):
    request.include('bootstrap')
    # We could further simplify by making bootstrap a bower dependency
    # Not working for some reason
    # request.include('taichi_style')
    with open('resources/index.html', 'r') as file_obj:
        result = file_obj.read()
    with open('log.csv', 'a') as log:
        log.write('I got a request at {}'.format(date.today()))
    return result

# Example of how to get static paths... but doesn't work with nested dirs...

# class Static(object):
#     def __init__(self, path):
#         self.path = path
#
# @App.path(model=Static, path='/static/{path}')
# def path_name(path):
#     return Static(path)
#
# @App.view(model=Static)
# def serve_static(self, request):
#     return self.path

def main():
    config=morepath.setup()
    config.scan()
    config.scan(static)
    config.commit()
    wsgi = App()
    morepath.run(wsgi)

if __name__ == '__main__':
    main()
