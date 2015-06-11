# taichi-videos
A simple web app to log when a user has watched one of the videos.

To use:

    python setup.py develop
    taichi-start

Note that you need to have a new-ish version of more.itsdangerous that supports
IdentityPolicy(secure=False) for the above script to work (otherwise, the
cookies won't work over local http).

I've implemented the right solution for "production" (enough so, anyway) in:
https://github.com/davclark/morepath-auth

But currently, that logic still needs to be copied over (tracked in issue #13).
