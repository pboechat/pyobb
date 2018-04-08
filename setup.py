#!/usr/bin/env python

from setuptools import setup


setup(name='pyobb',
      packages=['pyobb'],
      version='1.0.2',
      install_requires=['numpy>=1.12'],
      description='Python OBB Implementation',
      author='Pedro Boechat',
      author_email='pboechat@gmail.com',
      url='https://github.com/pboechat/pyobb',
      download_url = 'https://github.com/pboechat/pyobb/archive/1.0.2.tar.gz',
      keywords = ['obb', 'computational-geometry', 'oriented-bounding-box'])
