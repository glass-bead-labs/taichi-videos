from setuptools import setup, find_packages

setup(name='taichi_videos',
      packages=find_packages(),
      install_requires=[
         'morepath'
      ],
      entry_points={
         'console_scripts': [
          'taichi-start = taichi_videos.main:main'
          ]
      })
