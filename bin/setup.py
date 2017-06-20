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


setup(name='pyobb_demos',
      packages=['pyobb_demos'],
      version='0.0',
      install_requires=get_requirements(),
      entry_points={
          'console_scripts': [
              'pyobb_2d_demo = pyobb_demos.2d_demo:main',
              'pyobb_3d_demo = pyobb_demos.3d_demo:main'
          ]
      },
      description='Python OBB Demos',
      author='Pedro Boechat',
      author_email='pboechat@gmail.com',
      url='https://github.com/pboechat/pyobb/pyobb_demos')
