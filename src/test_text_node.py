import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


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

########################## TEXT NODE - TO HTML CODE CONVERTER TESTS ################################

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        text_node = TextNode("Sturm Graz allez!", TextType.BOLD)
        html_node = LeafNode("b", "Sturm Graz allez!")
        self.assertEqual(text_node_to_html_node(text_node).value, html_node.value)
    
    def test_link(self):
        text_node = TextNode("Sturm Graz allez!", TextType.LINK, "http://www.sksturm.at")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.props, {"href": "http://www.sksturm.at"})
        self.assertEqual(html_node.tag, "a")
    
    def test_image(self):
        text_node = TextNode("Sturm Graz allez!", TextType.IMAGE, "/images/SkSturm/Meisterfeier.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.props, {"src": "/images/SkSturm/Meisterfeier.jpg", "alt": "Sturm Graz allez!"})
        self.assertEqual(html_node.tag, "img")

if __name__ == "__main__":
    unittest.main()