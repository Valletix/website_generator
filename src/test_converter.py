import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode
from inline_converter import *


class TestConverter(unittest.TestCase):

    def test_italic(self):
        nodes = [TextNode("Der _SK Sturm_ ist wieder da!", TextType.TEXT), TextNode("Der _SK Rapid_ wird wieder verlieren!", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[4].text_type, TextType.ITALIC)

    
    def test_multiple_italic(self):
        nodes = [TextNode("Der _SK Sturm_ ist _wieder_ da!", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
           [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
          ],
            new_nodes,
        )
    
    def test_empty_string_between_delimiters(self):
        node = TextNode("This is an ** ** empty bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode(" ", TextType.BOLD),
                TextNode(" empty bold", TextType.TEXT),
            ], new_nodes
        )

    def test_just_bold(self):
        node = TextNode("**STURM GRAZ**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [TextNode("STURM GRAZ", TextType.BOLD)], new_nodes
        )

    def test_double_bold(self):
        node = TextNode("**STURM GRAZ** **ALLEZ**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [TextNode("STURM GRAZ", TextType.BOLD), 
             TextNode(" ", TextType.TEXT),
             TextNode("ALLEZ", TextType.BOLD) ], new_nodes
        )

    def test_bold_instant_italic(self):
        node = TextNode("**STURM GRAZ** _ALLEZ_", TextType.TEXT)
        bolded_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        italic_nodes = split_nodes_delimiter(bolded_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [TextNode("STURM GRAZ", TextType.BOLD), 
             TextNode(" ", TextType.TEXT),
             TextNode("ALLEZ", TextType.ITALIC)], italic_nodes
        )


    
################# TEST IMAGE & LINK EXTRACTION ######################

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_alt(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [[!link]](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("[!link]", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    
    def test_extract_markdown_links_no_alt(self):
        matches = extract_markdown_links(
            "This is text with a [](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)
        

    def test_extract_markdown_links_not_images(self):
        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    
    def test_extract_markdown_images_not_links(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif")], matches)
    
################# TEST IMAGE & LINK NODE-CONVERSION ######################

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
               ),
            ],
            new_nodes, 
        )


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_NO_images(self):
        node = TextNode(
            "This is text with a wrong [image](https://i.imgur.com/zjjcJKZ.png) and another wrong [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a wrong [image](https://i.imgur.com/zjjcJKZ.png) and another wrong [second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_one_image_rest(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another wrong [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                            
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another wrong [second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),

            ],
            new_nodes,
        )


    def test_split_one_image_one_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        image_nodes = split_nodes_image([node])
        link_nodes = split_nodes_link(image_nodes)

        self.assertListEqual(
            [
                            
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),

            ],
            link_nodes,
        )


################# TEST FINISHED CONVERTER ########################

    def test_convert_md_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], nodes
        )
if __name__ == "__main__":
    unittest.main()