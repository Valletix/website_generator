from textnode import *
from htmlnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter, 2)
        sub_list = []
        if len(split_node) == 2:
            raise Exception (f"Incorrect Markdown syntax. Maybe you forgot a {delimiter}?")
        if len(split_node) == 3:
            if split_node[0] != "": 
                sub_list.append(TextNode(split_node[0], TextType.TEXT))
            sub_list.append(TextNode(split_node[1], text_type))
            if split_node[2] != "":
                sub_list.extend(split_nodes_delimiter([TextNode(split_node[2], TextType.TEXT)], delimiter, text_type))   
        else:
            new_nodes.extend([TextNode(split_node[0], TextType.TEXT)])
        new_nodes.extend(sub_list)
    return new_nodes



def extract_markdown_images(text):
    tuple_list = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return tuple_list  

def extract_markdown_links(text):
    tuple_list = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return tuple_list


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = re.split(r"\!\[(.*?)\]\((.*?)\)", node.text, 1)
        sub_list = []
        if len(split_node) == 4:
            if split_node[0] != "": 
                sub_list.append(TextNode(split_node[0], TextType.TEXT))
            sub_list.append(TextNode(split_node[1], TextType.IMAGE, split_node[2]))
            if split_node[3] != "":
                sub_list.extend(split_nodes_image([TextNode(split_node[3], TextType.TEXT)]))  
        else:
            sub_list.extend([TextNode(split_node[0], TextType.TEXT)])
        new_nodes.extend(sub_list)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = re.split(r"(?<!!)\[(.*?)\]\((.*?)\)", node.text, 1)
        sub_list = []
        if len(split_node) == 4:
            if split_node[0] != "": 
                sub_list.append(TextNode(split_node[0], TextType.TEXT))
            sub_list.append(TextNode(split_node[1], TextType.LINK, split_node[2]))
            if split_node[3] != "":
                sub_list.extend(split_nodes_link([TextNode(split_node[3], TextType.TEXT)]))  
        else:
            sub_list.extend([TextNode(split_node[0], TextType.TEXT)])
        new_nodes.extend(sub_list)
    return new_nodes




def text_to_textnodes(text):
    split_links = split_nodes_link([TextNode(text,TextType.TEXT)])
    split_images = split_nodes_image(split_links)
    split_italics = split_nodes_delimiter(split_images, "_", TextType.ITALIC)
    split_bolds = split_nodes_delimiter(split_italics, "**", TextType.BOLD)
    split_code = split_nodes_delimiter(split_bolds, "`", TextType.CODE)
    return split_code
