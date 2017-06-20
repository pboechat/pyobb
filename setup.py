#!/usr/bin/env python

from distutils.core import setup


def get_requirements():
    with open('requirements.txt', 'r') as requirements_file:
        lines = requirements_file.readlines()
    requirements = []
    for line in lines:
        if line.startswith('#'):
            continue
        requirements.append(line.strip())
    return requirements


setup(name='pyobb',
      packages=['pyobb'],
      version='0.0',
      install_requires=get_requirements(),
      description='Python OBB Implementation',
      author='Pedro Boechat',
      author_email='pboechat@gmail.com',
      url='https://github.com/pboechat/pyobb')
