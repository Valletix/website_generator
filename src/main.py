from textnode import *

def main():
    link_node = TextNode("This is some anchor text", TextType.BOLD, "https://www.boot.dev")
    text_node = TextNode("Some text to play with fire", TextType.NORMAL)
    print(link_node)
    print(text_node)

main()