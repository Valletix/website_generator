import unittest
from markdown_blocks import *
import textwrap



class TestConverter(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here This is the same paragraph on a new line",
                "- This is a list - with items",
            ],
        )


    def test_blocktype_quote(self):
        mdblock =textwrap.dedent(""" 
        >This is a quote 
        >This is a quote  
        >This is a quote
        """).strip()
        block_type = block_to_blocktype(mdblock)
        self.assertEqual(block_type, BlockType.QUOTE)

    
    def test_blocktype_too_many_headings(self):
        mdblock =textwrap.dedent(""" 
        ####### This is a quote 
        """).strip()
        block_type = block_to_blocktype(mdblock)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_blocktype_heading(self):
        mdblock =textwrap.dedent(""" 
        #### This is a quote 
        """).strip()
        block_type = block_to_blocktype(mdblock)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_blocktype_code(self):
        mdblock = textwrap.dedent(""" 
        ```
        this is some code
        ```
        """).strip()
        block_type = block_to_blocktype(mdblock)
        self.assertEqual(block_type, BlockType.CODE)

    def test_blocktype_ordered_list(self):
        mdblock = textwrap.dedent(""" 
        1. I like cheese
        2. I hate apples
        3. Sturm wird Meister
        
        """).strip()
        block_type = block_to_blocktype(mdblock)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_blocktype_unordered_list(self):
        mdblock = textwrap.dedent(""" 
        - I like cheese
        - I hate apples
        - Sturm wird Meister
        """).strip()
        block_type = block_to_blocktype(mdblock)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)



    #################TEST FINISHED BLOCK NODES###################

    def test_paragraphs(self):
        md = textwrap.dedent("""
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """).strip()
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = textwrap.dedent("""
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """).strip()
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_heading(self):
        md = textwrap.dedent("""
        # This is a heading

        ## This is a smaller heading

        ### And even smaller
        """).strip()
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h2>This is a smaller heading</h2><h3>And even smaller</h3></div>",
        )
    def test_quote_block(self):
        md = textwrap.dedent("""
        > This is a quote
        > with multiple lines
        > and **bold** text
        """).strip()
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and <b>bold</b> text</blockquote></div>",
        )


    def test_unordered_list(self):
        md =textwrap.dedent("""
        - First item
        - Second item with _italic_
        - Third item with `code`
        """).strip()
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md =textwrap.dedent("""
        1. First item
        2. Second item with _italic_
        3. Third item with `code`
        """).strip()
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ol></div>",
        )




if __name__ == "__main__":
    unittest.main()