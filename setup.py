from setuptools import setup, find_packages

setup(name='taichi_videos',
      packages=find_packages(),
      install_requires=[
           'morepath>=0.10',
           'more.static',
           'more.itsdangerous',
           'more.jinja2',
           'werkzeug'
      ],
      dependency_links=[
          'http://github.com/morepath/more.itsdangerous/tarball/master#'
          'egg=more.itsdangerous-0.0.2dev',
      ],
      entry_points={
          'console_scripts': [
              'taichi-start = taichi_videos.develop:develop'
          ]
      })
