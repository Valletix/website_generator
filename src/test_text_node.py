import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_notEq(self):
        node = TextNode("Der SK Sturm ist wieder da!", TextType.NORMAL, url = "http://www.sksturm.at")
        node2 = TextNode("Der SK Sturm ist wieder da!", TextType.ITALIC, url = "http://www.sksturm.at")
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("Der SK Sturm ist wieder da!", TextType.NORMAL, url = None)
        node2 = TextNode("Der SK Sturm ist wieder da!", TextType.ITALIC, url = "http://www.sksturm.at")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()