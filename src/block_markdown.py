from textnode import (TextNode, text_node_to_html_node)
from htmlnode import (ParentNode, LeafNode)
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul = "unordered_list"
block_type_ol = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        filtered_blocks.append(block.strip())
    return filtered_blocks


def block_to_block_type(block):
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading

    lines = block.split("\n")

    if (
        len(lines) > 1
        and lines[0].startswith("```")
        and lines[-1].startswith("```")
    ):
        return block_type_code

    if lines[0].startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote

    if lines[0].startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ul

    if lines[0].startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ul

    if lines[0].startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ol

    return block_type_paragraph


def text_to_html_children(text):
    text_nodes = text_to_textnodes(text)
    html_children = []
    for text_node in text_nodes:
        html_children.append(text_node_to_html_node(text_node))
    return html_children


def block_to_paragraph(block):
    lines = block.split("\n")
    text = " ".join(lines)
    return ParentNode("p", text_to_html_children(text))


def block_to_heading(block):
    tag_level = 0
    for char in block:
        if char == "#":
            tag_level += 1
        else:
            break
    if tag_level + 1 >= len(block):
        raise ValueError("Invalid heading")
    text = block[tag_level+1:]
    return ParentNode(f"h{tag_level}", text_to_html_children(text))


def block_to_ul(block):
    lines = block.split("\n")
    html_children = []
    for line in lines:
        list_item_children = text_to_html_children(line[2:])
        html_children.append(ParentNode("li", list_item_children))
    return ParentNode("ul", html_children)


def block_to_ol(block):
    lines = block.split("\n")
    html_children = []
    for line in lines:
        list_item = line.split(" ", 1)
        list_item_children = text_to_html_children(list_item[1])
        html_children.append(ParentNode("li", list_item_children))
    return ParentNode("ol", html_children)


def block_to_quote(block):
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        if not line.startswith("> "):
            raise ValueError("Invalid quote block")
        quote_lines.append(line.strip(">").strip())
    html_children = text_to_html_children(" ".join(quote_lines))
    return ParentNode("blockquote", html_children)


def block_to_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    html_children = text_to_html_children(block[4:-3].strip())
    return ParentNode("pre", [ParentNode("code", html_children)])


def markdown_to_html_node(markdown):
    block = markdown_to_blocks(markdown)
    html_nodes = []
    for block in block:
        block_type = block_to_block_type(block)
        if block_type == block_type_paragraph:
            html_nodes.append(block_to_paragraph(block))
        elif block_type == block_type_heading:
            html_nodes.append(block_to_heading(block))
        elif block_type == block_type_quote:
            html_nodes.append(block_to_quote(block))
        elif block_type == block_type_code:
            html_nodes.append(block_to_code(block))
        elif block_type == block_type_ul:
            html_nodes.append(block_to_ul(block))
        elif block_type == block_type_ol:
            html_nodes.append(block_to_ol(block))
        else:
            raise ValueError("Invalid block type")
    return ParentNode("div", html_nodes)
