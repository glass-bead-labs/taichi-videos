# Werkzeug is only a dependency for development
# It's the easiest way (right now) to get reloading when code changes
import morepath
from werkzeug.serving import run_simple
from more.itsdangerous import IdentityPolicy
from .app import App


class TaiChiDevel(App):
    pass


@TaiChiDevel.identity_policy()
def get_identity_policy():
    return IdentityPolicy(secure=False)


def develop():
    morepath.autosetup()
    run_simple('localhost', 5000, TaiChiDevel(), use_reloader=True)
               # We apparently aren't supposed to do this
               # Plus, I can't seem to install a working PyOpenSSL - I quit
               # ssl_context='adhoc')
