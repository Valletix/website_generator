import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    
    def test_props_to_html_one_prop(self):
        node = HTMLNode("a", "Click me", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    
    def test_props_to_html_multiple_props(self):
        node = HTMLNode("a", "Click me", props={"href": "https://example.com", "target": "_blank"})
        # Note that dict order isn't guaranteed, so you might need a more flexible check
        # or ensure your props_to_html handles props in a consistent order
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hier regiert der SK Sturm!",{'href': 'http://www.sksturm.at'})
        self.assertEqual(node.to_html(), '<a href="http://www.sksturm.at">Hier regiert der SK Sturm!</a>')


    def test_leaf_to_html_img(self):
        node = LeafNode("img", "SK Sturm", {"src": "Ordner/Unterordner/Meisterfeier.jpg", "alt": "Ein Bild der großartigen Meisterfeier"})
        self.assertEqual(node.to_html(), '<img src="Ordner/Unterordner/Meisterfeier.jpg" alt="Ein Bild der großartigen Meisterfeier" />')

if __name__ == "__main__":
    unittest.main()