from setuptools import setup, find_packages

setup(name='taichi_videos',
      packages=find_packages(),
      install_requires=[
         'morepath',
         'more.static',
         'more.itsdangerous',
      ],
   dependency_links =
      ['http://github.com/seantis/more.itsdangerous/tarball/master#egg=more.itsdangerous-dev'],
      entry_points={
         'console_scripts': [
          'taichi-start = taichi_videos.main:main'
          ]
      })
