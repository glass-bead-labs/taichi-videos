import morepath

from werkzeug.serving import run_simple

from .app import App
from .videos import videos
from .login import ViewPermission
# Only for side-effects (noqa disables linter warning)
from . import static  # noqa


# Site root


@App.path(path='/')
class Root(object):
    pass


@App.view(model=Root, permission=ViewPermission)
def hello_word(self, request):
    # if not logged in, want to:
    # return morepath.redirect(request.link(login))
    return morepath.redirect(request.link(videos['14']))


# def generate_template_key_value(src):
#     with open(src) as csvfile:
#         reader = csv.reader(csvfile)
#         mydict = {row[0]: row[1] for row in reader}
#     return mydict


# def main():
#     # logging.basicConfig(filename='log/events.csv', level=logging.INFO)
#
#     # Now configuring to use autosetup
#     # config=morepath.setup()
#     # config.scan()
#     # config.scan(static)
#     # config.commit()
#     morepath.autosetup()
#     wsgi = App()
#     # morepath.run(wsgi)
#     run_simple('localhost', 5000, wsgi, use_reloader=True)
