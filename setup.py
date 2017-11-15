# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='Clerk Tools',
    version='0.1',
    description='Handy LDS clerk scripts',
    author='Eric Smith',
    author_email='eric@esmithy.net',
    license='MIT',
    packages=['clerk', 'tests'],
    zip_safe=True,
    entry_points={
       'console_scripts': [
           'clerk = clerk.__main__:main'
       ]
    },
)
