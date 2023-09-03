# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='FlavourSync',
    version='0.1.0',
    description='A restaurant management software made by Bhaskar for a school project, but will be worked upon upto his desire',
    long_description=readme,
    author='Bhaskar Patel',
    author_email='patel.bhaskar09@gmail.com',
    url='https://github.com/BinaryBhaskar/restaurant',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
