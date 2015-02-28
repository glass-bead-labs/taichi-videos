import morepath

class App(morepath.App):
	pass

@App.path(path='')
class Root(object):
	pass

@App.html(model=Root)
def hello_word(self, request):
	file_obj = open('index.html', 'r')
	result = file_obj.read()
	file_obj.close()
	return result #"Hello world!"

if __name__ == '__main__':
	config=morepath.setup()
	config.scan()
	config.commit()
	morepath.run(App())
