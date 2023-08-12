#!/usr/bin/env python3

import io
from os import path
from setuptools import setup, find_packages

pwd = path.abspath(path.dirname(__file__))

with io.open(path.join(pwd, 'README.md'), encoding='utf-8') as readme:
    desc = readme.read()

setup(
    name="insta-video-gen",
    version="1.0",
    description="A simple Insta meme compiler",
    long_description=desc,
    author="Raju Ghorai <rajughorai41410@gmail.com>",
    license='MIT License',
    packages=find_packages(),
    classifiers=[
        'Topic :: OSINT, Recon',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',

    ],
    entry_points={
        'console_scripts': [
            'memeify = insta-video-gen.app:main'
        ]
    },
    keywords=['insta-video-gen']
)
