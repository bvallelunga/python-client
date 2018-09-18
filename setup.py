#!/usr/bin/env python3

import os
from setuptools import setup, find_packages


def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
  name = "doppler-client",
  version = "0.0.1",
  author = "Doppler Team",
  author_email = "brian@doppler.market",
  description = "Official Doppler client for Python",
  license = "Apache License 2.0",
  long_description=read('README.md'),
  keywords = "doppler environment management api key keys secrets",
  url = "https://doppler.market",
  packages=find_packages(exclude=["tests", "templates", "experiments"]),
  install_requires=[
    "requests",
    "requests-futures"
  ],
  classifiers=[
    "Development Status :: 2 - Alpha",
    "Topic :: Utilities",
    "License :: Apache License 2.0"
  ],
  project_urls={
    'Bug Reports': 'https://github.com/DopplerMarket/python-client/issues',
    'Source': 'https://github.com/DopplerMarket/python-client',
  },
)