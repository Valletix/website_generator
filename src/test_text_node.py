import unittest

from textnode import TextNode, TextType
from converter import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_notEq(self):
        node = TextNode("Der SK Sturm ist wieder da!", TextType.TEXT, url = "http://www.sksturm.at")
        node2 = TextNode("Der SK Sturm ist wieder da!", TextType.ITALIC, url = "http://www.sksturm.at")
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("Der SK Sturm ist wieder da!", TextType.TEXT, url = None)
        node2 = TextNode("Der SK Sturm ist wieder da!", TextType.ITALIC, url = "http://www.sksturm.at")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()