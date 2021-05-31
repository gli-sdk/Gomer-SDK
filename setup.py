

from setuptools import setup, find_packages

import os.path
import platform

import sys

if sys.version_info < (3, 7, 4):
    sys.exit("Gomer SDK requires Python 3.7.4 or later")


curr = os.path.abspath(os.path.dirname(__file__))
data_files = []
if platform.system() == "Windows":
    data_files = [('gomer/libs', ['gomer/libs/LibGlproto64.dll']),
                  ('gomer/conf', ['gomer/conf/config.ini', 'gomer/conf/logger.ini'])]


setup(
    name='gomer',
    version='3.1.2',
    description="Gomer Python SDK",
    long_description=__doc__,

    long_description_content_type="text/markdown",
    keywords='glitech gomer sdk robot'.split(),
    # package_dir={'gomer'},
    packages=find_packages(),
    package_data={
        'gomer': ['README.md']
    },
    install_requires=[
        'numpy >= 1.18',
        'opencv-python >= 4.2',
    ],
    data_files=data_files
)
