#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='itunesfs',
    version='1.0.0.3',
    description='Script (python3 atm) for generating an iTunes Connect package (.itmsp) straight from your file system',
    long_description=open('README.rst', "r", encoding='utf-8-sig').read(),
    author='Petros Douvantzis',
    author_email='petrakeas@gmail.com',   
    packages=['itunesfslib'],
    entry_points = {
        'console_scripts': ['itunesfs=itunesfslib.command_line:main'],
    },
    url='https://github.com/evilwindowdog/itunesfs',
    license='MIT',
    install_requires=[
    "pyyaml"
    ],
    keywords=['itunesconnect', 'localization', 'yaml'],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
    ]
)
