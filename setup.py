from setuptools import setup, find_packages

setup(name='taichi_videos',
      packages=find_packages(),
      install_requires=[
         'morepath',
         'more.static',
         'more.itsdangerous',
         'more.jinja2', 
      ],
   dependency_links =
      ['http://github.com/seantis/more.itsdangerous/tarball/master#egg=more.itsdangerous-dev', "https://github.com/morepath/more.jinja2/tarball/master#egg=more.jinja2-dev"],
      entry_points={
         'console_scripts': [
          'taichi-start = taichi_videos.main:main'
          ]
      })
