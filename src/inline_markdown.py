import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not text_type_text:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid markdown syntax, formatted section not surrounded by delimiter \"{delimiter}\"")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], text_type_text))
            else:
                new_nodes.append(TextNode(sections[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not text_type_text:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        text_to_split = old_node.text
        for img in images:
            parts = text_to_split.split(f"![{img[0]}]({img[1]})", 1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown syntax for image")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], text_type_text))
            new_nodes.append(TextNode(img[0], text_type_image, img[1]))
            text_to_split = parts[1]
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not text_type_text:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        text_to_split = old_node.text
        for link in links:
            parts = text_to_split.split(f"[{link[0]}]({link[1]})", 1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown syntax for link")
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            text_to_split = parts[1]
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, text_type_text))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
