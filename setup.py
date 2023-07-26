#!/usr/bin/env python3

import os, re
from setuptools import setup

SRC = os.path.abspath(os.path.dirname(__file__))

def get_version():
    with open(os.path.join(SRC, 'app/__init__.py')) as f:
        for line in f:
            m = re.match("__version__ = '(.*)'", line)
            if m:
                return m.group(1)
    raise SystemExit("Could not find version string.")


setup(
    name='insta-video-gen',
    version=get_version()
)
