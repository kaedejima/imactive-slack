#!/usr/bin/env python

from distutils.core import setup
import setuptools

setup(name='imactive',
      version='1.0.0',
      description='Slack status tracker',
      author='KD',
      author_email='frogtoadie@gmail.com',
      install_requires=[
        'numpy',
        'opencv',
        'datetime',
        'dlib',
        'imutils',
        'os',
        'dotenv',
        'requests',
        'json',
        'time',
        'pandas',
        'slack'],
      url='https://github.com/kaedejima/imactive-slack',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*'])
     )