import os
import tempfile
import unittest

from Fill import strip_quotes, parse_dims, parse_point, parse_row, read_input, flood_fill, write_output


class TestFloodFill(unittest.TestCase):
    def test_strip_quotes(self):
        self.assertEqual(strip_quotes("'A'"), 'A')
        self.assertEqual(strip_quotes('"B"'), 'B')
        self.assertEqual(strip_quotes('C'), 'C')

    def test_parse_dims_and_point(self):
        self.assertEqual(parse_dims('10, 5'), (10, 5))
        self.assertEqual(parse_point('3, 9'), (3, 9))
        self.assertIsNone(parse_dims('invalid'))
        self.assertIsNone(parse_point('3'))

    def test_parse_row(self):
        self.assertEqual(parse_row("'Y','N','G'"), ['Y', 'N', 'G'])
        self.assertEqual(parse_row('Y, N, G'), ['Y', 'N', 'G'])

    def test_flood_fill_changes_region(self):
        matrix = [
            ['Y', 'Y', 'G'],
            ['Y', 'R', 'G'],
            ['G', 'G', 'G'],
        ]
        flood_fill(matrix, 0, 0, 'C')
        self.assertEqual(matrix, [
            ['C', 'C', 'G'],
            ['C', 'R', 'G'],
            ['G', 'G', 'G'],
        ])

    def test_read_input_and_write_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            in_file = os.path.join(tmpdir, 'input.txt')
            out_file = os.path.join(tmpdir, 'output.txt')
            data = """3,3
0,0
C
'Y','Y','G'
'Y','R','G'
'G','G','G'"""
            with open(in_file, 'w', encoding='utf-8') as f:
                f.write(data)

            parsed = read_input(in_file)
            self.assertIsNotNone(parsed)
            h, w, x, y, replacement, matrix = parsed
            self.assertEqual((h, w, x, y, replacement), (3, 3, 0, 0, 'C'))

            flood_fill(matrix, x, y, replacement)
            write_output(out_file, matrix)

            with open(out_file, 'r', encoding='utf-8') as f:
                result = f.read().strip()

            expected = "['C','C','G']\n['C','R','G']\n['G','G','G']"
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
