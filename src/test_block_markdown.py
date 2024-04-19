import unittest
from htmlnode import LeafNode, ParentNode
from block_markdown import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_ol,
    block_type_ul,
    block_type_quote,
    markdown_to_blocks,
    block_to_block_type,
    text_to_html_children,
    block_to_paragraph,
    block_to_heading,
    block_to_code,
    block_to_quote,
    block_to_ul,
    block_to_ol,
    markdown_to_html_node
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line



* This is a list
* with items
        """
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
            ]
        )

    def test_block_to_block_type(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ul)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_ol)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_text_to_html_children(self):
        text = "This is a paragraph with **bold** content"
        html_node = text_to_html_children(text)
        self.assertEqual(len(html_node), 3)
        self.assertIsNone(html_node[0].tag)
        self.assertIsInstance(html_node[0], LeafNode)

    def test_block_to_paragrah(self):
        block = "This is a markdown paragraph with **bold** and *italic*"
        html_node = block_to_paragraph(block)
        self.assertEqual(
            html_node.to_html(), "<p>This is a markdown paragraph with <b>bold</b> and <i>italic</i></p>")

    def test_block_to_paragraph_hyper(self):
        block = "This paragraph has ![image](test) and [link](test)"
        html_node = block_to_paragraph(block)
        self.assertEqual(
            html_node.to_html(), "<p>This paragraph has <img src=\"test\" alt=\"image\"></img> and <a href=\"test\">link</a></p>")

    def test_block_to_heading(self):
        block = "## This is a second level heading"
        html_node = block_to_heading(block)
        self.assertEqual(html_node.to_html(),
                         "<h2>This is a second level heading</h2>")

    def test_block_to_quote(self):
        block = "> This is a quote"
        html_node = block_to_quote(block)
        self.assertEqual(html_node.to_html(),
                         "<blockquote>This is a quote</blockquote>")

    def test_block_to_code(self):
        block = "```\nprint(\"Hello world\")\n```"
        html_node = block_to_code(block)
        self.assertEqual(
            html_node.to_html(), "<pre><code>print(\"Hello world\")</code></pre>")

    def test_block_to_ul(self):
        block = "* first item\n* second **item**"
        html_node = block_to_ul(block)
        self.assertEqual(
            html_node.to_html(), "<ul><li>first item</li><li>second <b>item</b></li></ul>")

    def test_block_to_ol(self):
        block = "1. first item\n2. second item"
        html_node = block_to_ol(block)
        self.assertEqual(
            html_node.to_html(), "<ol><li>first item</li><li>second item</li></ol>")

    def test_markdown_to_html(self):
        return
        markdown = """
# Heading

This is a paragraph

> This is a quote

1. This is a list
2. ordered

* This is a list
* with items

```
print("Hello world")
```
        """
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(
            html_node.to_html(),
            "<div>"
            + "<h1>Heading</h1>"
            + "<p>This is a paragraph</p>"
            + "<blockquote>This is a quote</blockquote>"
            + "<ol><li>This is a list</li><li>ordered</li></ol>"
            + "<ul><li>This is a list</li><li>with items</li></ul>"
            + "<pre><code>print(\"Hello world\")</code></pre>"
            + "</div>"
        )


if __name__ == "__main__":
    unittest.main()
