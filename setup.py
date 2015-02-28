from setuptools import setup, find_packages

setup(name='taichi_videos',
      packages=find_packages(),
      install_requires=[
         'morepath',
         'more.static',
      ],
      entry_points={
         'console_scripts': [
          'taichi-start = taichi_videos.main:main'
          ]
      })
