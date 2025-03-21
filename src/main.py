from textnode import *
from htmlnode import *

def main():
    link_node = TextNode("This is some anchor text", TextType.BOLD, "https://www.boot.dev")
    html_node= HTMLNode("a", "Nur der SK Sturm", props={"href": "http://www.sksturm.at","target": "_blank"})
    print(link_node)
    print(html_node)

main()