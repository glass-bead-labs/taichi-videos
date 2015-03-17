from setuptools import setup, find_packages

setup(name='taichi_videos',
      packages=find_packages(),
      install_requires=[
         'morepath',
         'more.static',
         'more.itsdangerous',
      ],
   dependency_links =
      ['http://github.com/seantis/more.itsdangerous/tarball/master#egg=more.itsdangerous-dev',
       'http://github.com/morepath/morepath/tarball/master#egg=morepath-0.10.dev0'],
      entry_points={
         'console_scripts': [
          'taichi-start = taichi_videos.main:main'
          ]
      })
