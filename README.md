# Bash-style brace expansion for Python

[![build-status-img]][build-status-url]

Implements Brace Expansion as described in [bash(1)][1], with the following
limitations:

  * A pattern containing unbalanced braces will raise an
    `UnbalancedBracesError` exception. In bash, unbalanced braces will either
    be partly expanded or ignored.

  * A mixed-case character range like `'{Z..a}'` or `'{a..Z}'` will not
    include the characters `` []^_` `` between `Z` and `a`.

`braceexpand` is tested with Python 2.7, and 3.6+

## Installation

Install the `braceexpand` package from pypi:

    $ pip install braceexpand

## Examples

The `braceexpand` function returns an iterator over the expansions generated
from a pattern.

~~~python
>>> from braceexpand import braceexpand

# Integer range
>>> list(braceexpand('item{1..3}'))
['item1', 'item2', 'item3']

# Character range
>>> list(braceexpand('{a..c}'))
['a', 'b', 'c']

# Sequence
>>> list(braceexpand('index.html{,.backup}'))
['index.html', 'index.html.backup']

# Nested patterns
>>> list(braceexpand('python{2.{5..7},3.{2,3}}'))
['python2.5', 'python2.6', 'python2.7', 'python3.2', 'python3.3']

# Prefixing an integer with zero causes all numbers to be padded to
# the same width.
>>> list(braceexpand('{07..10}'))
['07', '08', '09', '10']

# An optional increment can be specified for ranges.
>>> list(braceexpand('{a..g..2}'))
['a', 'c', 'e', 'g']

# Ranges can go in both directions.
>>> list(braceexpand('{4..1}'))
['4', '3', '2', '1']

# Numbers can be negative
>>> list(braceexpand('{2..-1}'))
['2', '1', '0', '-1']

# Unbalanced braces raise an exception.
>>> list(braceexpand('{1{2,3}'))
Traceback (most recent call last):
    ...
UnbalancedBracesError: Unbalanced braces: '{1{2,3}'

# By default, the backslash is the escape character.
>>> list(braceexpand(r'{1\{2,3}'))
['1{2', '3']

# Setting 'escape' to False disables backslash escaping.
>>> list(braceexpand(r'\{1,2}', escape=False))
['\\1', '\\2']
~~~

[1]: http://man7.org/linux/man-pages/man1/bash.1.html#EXPANSION
[build-status-url]: https://travis-ci.org/trendels/braceexpand
[build-status-img]: https://travis-ci.org/trendels/braceexpand.svg

## License

braceexpand is licensed under the MIT License. See the included file `LICENSE`
for details.
