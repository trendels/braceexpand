from distutils.core import setup
import re

version = re.search(r"^__version__ = '(.*)'",
                    open('braceexpand.py', 'r').read(), re.M).group(1)

setup(name='braceexpand',
      version=version,
      description="Bash-style brace expansion",
      long_description=open('README.rst').read(),
      classifiers=[
          'Programming Language :: Python',
          'License :: OSI Approved :: MIT License',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Text Processing',
          ],
      keywords='bash brace expansion',
      url='https://github.com/trendels/braceexpand',
      author='Stanis Trendelenburg',
      author_email='stanis.trendelenburg@gmail.com',
      license='MIT',
      py_modules=['braceexpand'],
      )

