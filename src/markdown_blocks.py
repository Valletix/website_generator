from enum import Enum
from htmlnode import *
from inline_converter import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_blocktype(md_block):

    def check_ordered_list(list):
        i = 1
        bool = False
        for line in list:
            bool = line.startswith(f"{i}. ")
            if bool is False:
                return False
            i += 1
        return bool


    lines = md_block.split("\n")
        
    if md_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if  len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if check_ordered_list(lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    new_blocks = []
    for block in split_blocks:
        new_lines = []
        for line in block.split("\n"):
            new_lines.append(line.strip())
        block_type = block_to_blocktype(block)
        if block_type not in [BlockType.CODE, BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST, BlockType.QUOTE]:
            new_blocks.append((" ".join(new_lines)).strip())
        else: 
            new_blocks.append(("\n".join(new_lines)).strip())
    return new_blocks


def markdown_to_html_node(md_file):
    md_blocks = markdown_to_blocks(md_file)
    block_list = []
    for block in md_blocks:
        block_type = block_to_blocktype(block)
        block_html_node = block_type_to_html_node(block, block_type)
        block_list.append(block_html_node)
    return ParentNode("div", block_list)
        

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def split_headings(block):
    split_hash_text = block.split(" ", 1)
    return (split_hash_text[0].count("#"), split_hash_text[1])

def get_tagremoved_quotes(block):
    split_quote_lines = block.split("\n")
    removed_md_quotes = []
    for quote_line in split_quote_lines:
        removed_md_quotes.append(quote_line.lstrip("> "))
    return " ".join(removed_md_quotes)

def get_unordered_list_items(block):
    list_items = []
    lines = block.split("\n")
    for item in lines:
        item_content = item.lstrip("- ")
        item_nodes = text_to_children(item_content)
        list_items.append(ParentNode("li", item_nodes))
    return list_items

def get_ordered_list_items(block):
    list_items = []
    lines = block.split("\n")
    for i, item in enumerate(lines):
        item_content = item.lstrip("0123456789. )")
        item_nodes = text_to_children(item_content)
        list_items.append(ParentNode("li", item_nodes))
    return list_items

    
def get_code(block):
    lines = block.split("\n")
    content_lines = lines[1:-1] if len(lines) > 2 else []
    return "\n".join(content_lines) + "\n"

def block_type_to_html_node(block, block_type):  
    match block_type:
        case BlockType.PARAGRAPH:
            text_nodes = text_to_children(block)
            return ParentNode("p", text_nodes)
        case BlockType.HEADING:
            level, content = split_headings(block)
            text_nodes = text_to_children(content)
            return ParentNode(f"h{level}", text_nodes)
        case BlockType.CODE:
            return ParentNode("pre",[LeafNode("code", get_code(block))])
        case BlockType.QUOTE:
            content = get_tagremoved_quotes(block)
            text_nodes = text_to_children(content)
            return ParentNode("blockquote", text_nodes)
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul",get_unordered_list_items(block))
        case BlockType.ORDERED_LIST:
            return ParentNode("ol",get_ordered_list_items(block))
        case _:
            raise Exception("Not a valid Type.")