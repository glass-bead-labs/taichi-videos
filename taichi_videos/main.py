import morepath
from more import static
import bowerstatic

## Set up our App

# class App(morepath.App):
class App(static.StaticApp):
    pass

## Basic Bower stuff

bower = bowerstatic.Bower()
# Currently configuring to look from directory where run
components = bower.components('app', 
                        '/home/dav/Projects/taichi-videos/bower_components')

@App.static_components()
def get_static_components():
        return components

## Site root

@App.path(path='static')
class Root(object):
        pass

@App.path(path='')
class Root(object):
    pass

#@App.static_components()
#def get_static_components():
#    return components

@App.html(model=Root)
def hello_word(self, request):
    request.include('bootstrap')
    # request.include('jquery/dist/jquery.min.js')
    with open('resources/index.html', 'r') as file_obj:
        result = file_obj.read()
    return result

class Static(object):
    def __init__(self, path):
        self.path = path

@App.path(model=Static, path='/static/{path}')
def path_name(path):
    return Static(path)

@App.view(model=Static)
def serve_static(self, request):
    return self.path

def main():
    config=morepath.setup()
    config.scan()
    config.scan(static)
    config.commit()
    wsgi = App()
    morepath.run(wsgi)

if __name__ == '__main__':
    main()
