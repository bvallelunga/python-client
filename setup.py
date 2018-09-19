#!/usr/bin/env python3

import os
from setuptools import setup, find_packages


def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
  name = "doppler-client",
  version = "0.0.6",
  author = "Doppler Team",
  author_email = "support@doppler.market",
  description = "Official Doppler client for Python",
  license = "Apache License 2.0",
  long_description=read('README.md'),
  long_description_content_type='text/markdown',
  keywords = "doppler environment management api key keys secrets",
  url = "https://github.com/DopplerHQ/python-client",
  packages=find_packages(exclude=["tests", "templates", "experiments"]),
  install_requires=[
    "requests",
    "requests-futures"
  ],
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Topic :: Utilities",
    "License :: OSI Approved :: Apache Software License"
  ],
  project_urls={
    'Bug Reports': 'https://github.com/DopplerHQ/python-client/issues',
    'Source': 'https://github.com/DopplerHQ/python-client',
  },
)