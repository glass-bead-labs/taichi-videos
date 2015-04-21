from csv import DictReader
import logging
from datetime import date

from .app import App
from .login import ViewPermission
from . import static  # noqa


class Video(object):

    def __init__(self, attribute_dict):
        self.attribute_dict = attribute_dict
        # This is an odd construct - discuss with Martjin & co.
        self.vidId = attribute_dict['id']

with open('resources/all-videos.csv') as csvfile:
    reader = DictReader(csvfile)
    videos = {row['id']: Video(row) for row in reader}


@App.path(model=Video, path='/video/{vidId}')
def get_video(vidId):
    return videos[vidId]


@App.html(model=Video, template="index.jinja2", permission=ViewPermission)
def video(self, request):
    request.include('bootstrap')
    request.include('taichi_style')

    logging.info('I got a request at {}'.format(date.today()))

    return self.attribute_dict
