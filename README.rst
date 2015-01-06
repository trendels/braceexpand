Bash-style brace expansion for Python
=====================================

|build-status-img|

Implements Brace Expansion as described in
`bash(1) <http://man7.org/linux/man-pages/man1/bash.1.html#EXPANSION>`__,
with the following limitations:

-  A pattern containing unbalanced braces will raise an
   ``UnbalancedBracesError`` exception. In bash, unbalanced braces will
   either be partly expanded or ignored.

-  A mixed-case character range like ``'{Z..a}'`` or ``'{a..Z}'`` will
   not include the characters ``[]^_``` between ``Z`` and ``a``.

The ``braceexpand`` function returns an iterator over the expansions
generated from a pattern.

Example:

.. code:: python

    >>> from braceexpand import braceexpand
    >>> list(braceexpand('python{2.{5..7},3.{2,3}}'))
    ['python2.5', 'python2.6', 'python2.7', 'python3.2', 'python3.3']

Installation
------------

Drop the ``braceexpand.py`` file into your project, or install the
``braceexpand`` package from pypi:

::

    $ pip install braceexpand

License
-------

braceexpand is licensed unter the MIT License. See the included file
``LICENSE`` for details.

.. |build-status-img| image:: https://travis-ci.org/trendels/braceexpand.svg
   :target: https://travis-ci.org/trendels/braceexpand
