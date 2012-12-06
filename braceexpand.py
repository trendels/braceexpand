"""Bash-style brace expansion"""
import re
import string
from itertools import chain, product

__version__ = '0.1.0'

__all__ = ['braceexpand', 'alphabet', 'alphabet_bash', 'USE_BASH_ALPHABET']

alphabet = string.uppercase + string.lowercase
alphabet_bash = string.uppercase + '[]^_`' + string.lowercase

USE_BASH_ALPHABET = False

# Even in 'bash' mode the extra punctuation characters between 'Z'
# and 'a' are not valid start or end points for a character range.
# This is consistent with Bash's behaviour.
int_range_re = re.compile(r'^(\d+)\.\.(\d+)(?:\.\.-?(\d+))?$')
char_range_re = re.compile(r'^([A-Za-z])\.\.([A-Za-z])(?:\.\.-?(\d+))?$')

def braceexpand(pattern):
    """braceexpand(pattern) --> iterator over generated strings

    Returns an iterator over the strings resulting from brace expansion
    of pattern. This behaves like Brace Expansion in as described in
    bash(1), with the following limitations:

    - Literal braces or commas can not be quoted using a backslash
      ('\\'). A backslash is treated like a regular character.

    - No expansion will be done if the pattern contains unbalanced
      braces. In this case the function will yield the original pattern.

    - By default, a character range that crosses the uppercase to
      lowercase boundary (e.g. '{Z..a}' or '{a..Z}') will not include
      the characters '[', ']', '^', '_', and '`' between 'Z' and 'a'
      like it does in bash.

      This behaviour can be enabled by setting the module-level variable
      USE_BASH_ALPHABET to True.

    Examples:

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
    >>> list(braceexpand('/usr/{ucb/{ex,edit},}'))
    ['/usr/ucb/ex', '/usr/ucb/edit', '/usr/']

    # Prefixing an integer with zero causes all numbers to be padded to the
    # same width.
    >>> list(braceexpand('{07..10}'))
    ['07', '08', '09', '10']

    # An optional increment can be specified for ranges.
    >>> list(braceexpand('{a..g..2}'))
    ['a', 'c', 'e', 'g']

    # The increment can be negative.
    >>> list(braceexpand('{10..4..-2}'))
    ['10', '8', '6', '4']

    # Unbalanced braces are not expanded (in bash(1), they often are):
    >>> list(braceexpand('{1}2,3}'))
    ['{1}2,3}']

    # In Bash, this would expand to "X Y Z [ ] ^ _ ` a b c"
    >>> list(braceexpand('{X..c}'))
    ['X', 'Y', 'Z', 'a', 'b', 'c']

    """
    return (_flatten(t) for t in parse_pattern(pattern))


def parse_pattern(pattern):
    # pattern -> product(*parts)
    if not ('{' in pattern and '}' in pattern
            and pattern.index('{') < pattern.rindex('}')):
        return iter([pattern])

    start = 0
    pos = 0
    bracketdepth = 0
    items = []

    #print 'pattern:', pattern
    while pos < len(pattern):
        if pattern[pos] == '{':
            if bracketdepth == 0 and pos > start:
                #print 'literal:', pattern[start:pos]
                items.append([pattern[start:pos]])
                start = pos
            bracketdepth += 1
        elif pattern[pos] == '}':
            bracketdepth -= 1
            if bracketdepth == 0:
                #print 'expression:', pattern[start+1:pos]
                items.append(parse_expression(pattern[start+1:pos]))
                start = pos + 1 # skip the closing brace
        pos += 1

    if bracketdepth != 0:
        return iter([pattern])

    if start < pos:
        #print 'literal:', pattern[start:]
        items.append([pattern[start:]])

    return product(*items)


def parse_expression(expr):
    int_range_match = int_range_re.match(expr)
    if int_range_match:
        return make_int_range(*int_range_match.groups())

    char_range_match = char_range_re.match(expr)
    if char_range_match:
        return make_char_range(*char_range_match.groups())

    return parse_sequence(expr)


def parse_sequence(seq):
    # sequence -> chain(*sequence_items)
    start = 0
    pos = 0
    bracketdepth = 0
    items = []

    while pos < len(seq):
        if seq[pos] == '{':
            bracketdepth += 1
        elif seq[pos] == '}':
            bracketdepth -= 1
        elif seq[pos] == ',' and bracketdepth == 0:
            items.append(parse_pattern(seq[start:pos]))
            start = pos + 1 # skip the comma
        pos += 1

    if bracketdepth != 0 or not items:
        return iter(['{' + seq + '}'])

    # part after the last comma (may be the empty string)
    items.append(parse_pattern(seq[start:]))
    return chain(*items)


def make_int_range(start, end, step=None):
    padding = max(len(s) for s in (start, end, '0') if s.startswith('0'))
    step = int(step) if step else 1
    start = int(start)
    end = int(end)
    range_ = xrange(start, end+1, step) if start < end else \
             xrange(start, end-1, -step)
    return (str(i).rjust(padding, '0') for i in range_)


def make_char_range(start, end, step=None):
    step = int(step) if step else 1
    letters = alphabet_bash if USE_BASH_ALPHABET else alphabet
    start = letters.index(start)
    end = letters.index(end)
    return letters[start:end+1:step] if start < end else \
           letters[start:end-1:-step]


def _flatten(t):
    l = []
    for item in t:
        if isinstance(item, tuple): l.extend(_flatten(item))
        else: l.append(item)
    return ''.join(l)


def test_brace_expansion():
    tests = {
            '{1,2}': ['1', '2'],
            '{1}': ['{1}'],
            '{1,2{}}': ['1', '2{}'],

            # Unbalanced braces
            '{{1,2}': ['{{1,2}'], # Bash: {1 {2
            '{1,2}}': ['{1,2}}'], # Bash: 1} 2}
            '{1},2}': ['{1},2}'], # Bash: 1} 2
            '{1,{2}': ['{1,{2}'], # Bash: {1,{2}
            '{}1,2}': ['{}1,2}'], # Bash: }1 2
            '{1,2{}': ['{1,2{}'], # Bash: {1,2{}
            '}{1,2}': ['}{1,2}'], # Bash: }1 }2
            '{1,2}{': ['{1,2}{'], # Bash: 1{ 2{

            '}{': ['}{'],
            'a{b,c}d{e,f}': ['abde', 'abdf', 'acde', 'acdf'],
            'a{b,c{d,e,}}': ['ab', 'acd', 'ace', 'ac'],
            'a{b,{c,{d,e}}}': ['ab', 'ac', 'ad', 'ae'],
            '{{a,b},{c,d}}': ['a', 'b', 'c', 'd'],
            '{7..10}': ['7', '8', '9', '10'],
            '{10..7}': ['10', '9', '8', '7'],
            '{1..5..2}': ['1', '3', '5'],
            '{5..1..2}': ['5', '3', '1'],
            '{07..10}': ['07', '08', '09', '10'],
            '{7..010}': ['007', '008', '009', '010'],
            '{a..e}': ['a', 'b', 'c', 'd', 'e'],
            '{a..e..2}': ['a', 'c', 'e'],
            '{e..a}': ['e', 'd', 'c', 'b', 'a'],
            '{e..a..2}': ['e', 'c', 'a'],
            '{1..a}': ['{1..a}'],
            '{a..1}': ['{a..1}'],
            '{1..1}': ['1'],
            '{a..a}': ['a'],
            '{,}': ['', ''],
    }
    bash_tests = {
            '{Z..a}': ['Z', '[', ']', '^', '_', '`', 'a'],
            '{a..Z}': ['a', '`', '_', '^', ']', '[', 'Z'],
    }
    default_tests = {
            '{Z..a}': ['Z', 'a'],
            '{a..Z}': ['a', 'Z'],
    }

    for pattern, result in tests.items() + default_tests.items():
        assert list(braceexpand(pattern)) == result

    global USE_BASH_ALPHABET
    USE_BASH_ALPHABET = True
    for pattern, result in tests.items() + bash_tests.items():
        assert list(braceexpand(pattern)) == result
    USE_BASH_ALPHABET = False

    return "tests pass"


if __name__ == '__main__':
    print test_brace_expansion()
    import doctest
    failed, total = doctest.testmod()
    print "doctest: %d of %d tests pass" % (total - failed, total)

