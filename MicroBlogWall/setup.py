#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='MicroBlogWall',
    version=0.1,
    description='newswall',
    author='han',
    install_requires=[
        'BeautifulSoup4',
        'requests',
        'tornado',
    ],
    entry_points={
        'console_scripts': [
            'newswall = main:main',
        ],
    },
)
