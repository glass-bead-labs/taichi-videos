import morepath

class App(morepath.App):
    pass

@App.path(path='')
class Root(object):
    pass

#@App.static_components()
#def get_static_components():
#    return components

@App.html(model=Root)
def hello_word(self, request):
    file_obj = open('index.html', 'r')
    result = file_obj.read()
    file_obj.close()
    #local = bower.local_components('local', components)
    #local.component('../resources/static/style', version=None)
    #local.component('../resources/static/bootstrap-3.3.2-dist', version=None)
    return result #"Hello world!"

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
    config.commit()
    morepath.run(App())

if __name__ == '__main__':
    main()
