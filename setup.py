import re

from setuptools import setup

with open('braceexpand.py') as f:
    version = re.findall(r"^__version__ = '(.*)'", f.read(), re.M)[0]

with open('README.rst') as f:
    README = f.read()

setup(
    name='braceexpand',
    version=version,
    author='Stanis Trendelenburg',
    author_email='stanis.trendelenburg@gmail.com',
    py_modules=['braceexpand'],
    url='https://github.com/trendels/braceexpand',
    license='MIT',
    description='Bash-style brace expansion for Python',
    long_description=README,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
