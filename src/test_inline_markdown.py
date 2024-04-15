import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links
)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code
)


class TestInlineMarkdown(unittest.TestCase):

    def test_italic(self):
        node = TextNode("This is *italic* text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" text", text_type_text)
            ]
        )

    def test_bold(self):
        node = TextNode("This is **bold** text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" text", text_type_text)
            ]
        )

    def test_code(self):
        node = TextNode("This is `code` text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("code", text_type_code),
                TextNode(" text", text_type_text)
            ]
        )

    def test_multiword(self):
        node = TextNode(
            "This is **a phrase** with two **bolded sections**", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("a phrase", text_type_bold),
                TextNode(" with two ", text_type_text),
                TextNode("bolded sections", text_type_bold),
            ]
        )

    def test_multinode(self):
        node1 = TextNode("The **first** node", text_type_text)
        node2 = TextNode("The **second** node", text_type_text)
        new_nodes = split_nodes_delimiter([node1, node2], "**", text_type_bold)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("The ", text_type_text),
                TextNode("first", text_type_bold),
                TextNode(" node", text_type_text),
                TextNode("The ", text_type_text),
                TextNode("second", text_type_bold),
                TextNode(" node", text_type_text),
            ]
        )

    def test_not_text(self):
        node = TextNode("An italic section", text_type_italic)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            new_nodes,
            [TextNode("An italic section", text_type_italic)]
        )

    def test_extra_delimiter(self):
        node = TextNode("***A strange italic section***", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            new_nodes,
            [TextNode("A strange italic section", text_type_italic)]
        )

    def test_raise_error(self):
        with self.assertRaises(ValueError):
            node = TextNode("A malformed **bold phrase", text_type_text)
            new_nodes = split_nodes_delimiter([node], "**", text_type_bold)

    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is an image ![alt](https://www.boot.dev)")
        self.assertListEqual(
            matches,
            [("alt", "https://www.boot.dev")]
        )

    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is [a link](https://www.boot.dev)")
        self.assertListEqual(
            matches,
            [("a link", "https://www.boot.dev")]
        )


if __name__ == "__main__":
    unittest.main()
