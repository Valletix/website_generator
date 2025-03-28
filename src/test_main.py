import unittest
import textwrap
from main import extract_title


class TestConverter(unittest.TestCase):

    def test_return_heading(self):
        md = textwrap.dedent("""
        # This is a heading

        ## This is a smaller heading

        ### And even smaller
        """).strip()
        line = extract_title(md)
        self.assertEqual(line, "This is a heading")

    def test_return_heading_space_right(self):
        md = textwrap.dedent("""
        ### This is a heading
        # This is another heading            
        ## This is a smaller heading

        ### And even smaller
        """).strip()
        line = extract_title(md)
        self.assertEqual(line, "This is another heading")

    def test_return_no_heading(self):
        md = textwrap.dedent("""
        ### This is a heading        
        ## This is a smaller heading

        ### And even smaller
        """).strip()
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()