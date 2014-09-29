# -*- coding: utf-8 -*-
from setuptools import setup
import sys

#pandoc -o README.rst README.md

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
    sys.exit(1)

setup(
    name='itunesfs',
    version='1.0.0.9',
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
    "pyyaml",
    "xtermcolor"
    ],
    keywords=['itunesconnect', 'localization', 'yaml','apple','itunes','iTMStransporter','iOS'],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
    ]
)
