#!/usr/bin/env python

from setuptools import setup

setup(
    name='x-selection-pipe',
    version='0.1.0.0',
    description=(
        "A simple clipboard-monitor intended as a data source in shell "
        "pipelines."
    ),
    author="Sebastian Reuße",
    author_email='seb@wirrsal.net',
    url='https://github.com/eigengrau/x-selection-pipe',
    packages=[
        'xselection',
        'xselection.util'
    ],
    package_dir={'': 'src'},
    install_requires=['pygobject >=3.16, <3.25'],
    license="GPL3",
    entry_points={
        'console_scripts': [
            'xselection-pipe = xselection.cli:main'
        ],
    }
)
