#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup


setup(
    name='django-signage',
    version='0.0.1',
    description='A lightweight web-based digital signage application',
    license='BSD',
    author='Jason Bittel',
    author_email='jason.bittel@gmail.com',
    url='https://github.com/jbittel/django-signage',
    download_url='https://github.com/jbittel/django-signage',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
