import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a different text node", text_type_italic)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node",
                        text_type_bold, "https://boot.dev")
        node2 = TextNode("This is a text node",
                         text_type_bold, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", text_type_bold)
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_bold,
                        "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, bold, https://www.boot.dev)",
            repr(node)
        )


if __name__ == "__main__":
    unittest.main()
