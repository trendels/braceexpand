"""Bash-style brace expansion"""
import unittest
import braceexpand

class BraceExpand(unittest.TestCase):
    tests = [
            ('{1,2}', ['1', '2']),
            ('{1}', ['{1}']),
            ('{1,2{}}', ['1', '2{}']),
            ('}{', ['}{']),
            ('a{b,c}d{e,f}', ['abde', 'abdf', 'acde', 'acdf']),
            ('a{b,c{d,e,}}', ['ab', 'acd', 'ace', 'ac']),
            ('a{b,{c,{d,e}}}', ['ab', 'ac', 'ad', 'ae']),
            ('{{a,b},{c,d}}', ['a', 'b', 'c', 'd']),
            ('{7..10}', ['7', '8', '9', '10']),
            ('{10..7}', ['10', '9', '8', '7']),
            ('{1..5..2}', ['1', '3', '5']),
            ('{5..1..2}', ['5', '3', '1']),
            ('{07..10}', ['07', '08', '09', '10']),
            ('{7..010}', ['007', '008', '009', '010']),
            ('{a..e}', ['a', 'b', 'c', 'd', 'e']),
            ('{a..e..2}', ['a', 'c', 'e']),
            ('{e..a}', ['e', 'd', 'c', 'b', 'a']),
            ('{e..a..2}', ['e', 'c', 'a']),
            ('{1..a}', ['{1..a}']),
            ('{a..1}', ['{a..1}']),
            ('{1..1}', ['1']),
            ('{a..a}', ['a']),
            ('{,}', ['', '']),
            ('{Z..a}', ['Z', 'a']),
            ('{a..Z}', ['a', 'Z']),
    ]

    unbalanced_tests = [
            # Unbalanced braces
            ('{{1,2}', ['{{1,2}']), # Bash: {1 {2
            ('{1,2}}', ['{1,2}}']), # Bash: 1} 2}
            ('{1},2}', ['{1},2}']), # Bash: 1} 2
            ('{1,{2}', ['{1,{2}']), # Bash: {1,{2}
            ('{}1,2}', ['{}1,2}']), # Bash: }1 2
            ('{1,2{}', ['{1,2{}']), # Bash: {1,2{}
            ('}{1,2}', ['}{1,2}']), # Bash: }1 }2
            ('{1,2}{', ['{1,2}{']), # Bash: 1{ 2{
    ]

    escape_tests = [
            ('\\{1,2}', ['\\1', '\\2'], ['{1,2}']),
            ('{1\\,2}', ['1\\', '2'], ['{1,2}']),
            ('{1,2\\}', ['1', '2\\'], ['{1,2}']),

            ('\\}{1,2}', ['\\}{1,2}'], ['}1', '}2']),
            ('\\{{1,2}', ['\\{{1,2}'], ['{1', '{2']),
            ('{1,2}\\}', ['{1,2}\\}'], ['1}', '2}']),
            ('{1,2}\\{', ['{1,2}\\{'], ['1{', '2{']),

            ('{\\,1,2}', ['\\', '1', '2'], [',1', '2']),
            ('{1\\,,2}', ['1\\', '', '2'], ['1,', '2']),
            ('{1,\\,2}', ['1', '\\', '2'], ['1', ',2']),
            ('{1,2\\,}', ['1', '2\\', ''], ['1', '2,']),

            ('\\\\{1,2}', ['\\\\1', '\\\\2'], ['\\1', '\\2']),

            ('\\{1..2}', ['\\1', '\\2'], ['{1..2}']),
    ]

    def test_braceexpand(self):
        for pattern, expected in self.tests:
            result = list(braceexpand.braceexpand(pattern))
            self.assertEqual(expected, result)

    def test_braceexpand_unbalanced(self):
        for pattern, expected in self.unbalanced_tests:
            result = list(braceexpand.braceexpand(pattern))
            self.assertEqual(expected, result)

    def test_braceexpand_escape(self):
        for pattern, expected_false, expected_true in self.escape_tests:
            result_false = list(braceexpand.braceexpand(pattern, False))
            result_true = list(braceexpand.braceexpand(pattern, True))
            self.assertEqual(expected_false, result_false)
            self.assertEqual(expected_true, result_true)


class BashAlphabet(unittest.TestCase):
    bash_tests = [
            ('{Z..a}', ['Z', '[', ']', '^', '_', '`', 'a']),
            ('{a..Z}', ['a', '`', '_', '^', ']', '[', 'Z']),
    ]

    def setUp(self):
        braceexpand.USE_BASH_ALPHABET = True

    def tearDown(self):
        braceexpand.USE_BASH_ALPHABET = False

    def test_braceexpand_use_bash_alphabet(self):
        for pattern, expected in self.bash_tests:
            result = list(braceexpand.braceexpand(pattern))
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
