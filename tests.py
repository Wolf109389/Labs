import unittest
from lab import search_finite_automaton 

class TestFiniteAutomatonSearch(unittest.TestCase):
    
    def test_basic_match(self):
        self.assertEqual(search_finite_automaton("hello world", "hello"), [0])
        self.assertEqual(search_finite_automaton("hello world", "world"), [6])

    def test_multiple_occurrences(self):
        self.assertEqual(search_finite_automaton("abracadabra", "abra"), [0, 7])
        self.assertEqual(search_finite_automaton("banana", "a"), [1, 3, 5])

    def test_overlapping_patterns(self):
        self.assertEqual(search_finite_automaton("aaaaa", "aa"), [0, 1, 2, 3])
        self.assertEqual(search_finite_automaton("ababa", "aba"), [0, 2])

    def test_no_match(self):
        self.assertEqual(search_finite_automaton("python", "java"), [])

    def test_empty_inputs(self):
        self.assertEqual(search_finite_automaton("", "pattern"), [])
        self.assertEqual(search_finite_automaton("text", ""), [])

    def test_case_sensitivity(self):
        self.assertEqual(search_finite_automaton("Python", "python"), [])

if __name__ == '__main__':
    unittest.main()