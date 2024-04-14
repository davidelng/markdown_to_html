import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_html_props(self):
        node = HTMLNode(
            "h1",
            "Title",
            None,
            {"class": "title", "id": "heading"}
        )
        self.assertEqual(
            " class=\"title\" id=\"heading\"",
            node.props_to_html()
        )

    def test_leaf_node(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(
            node.to_html(),
            "<p>This is a paragraph</p>"
        )

    def test_leaf_node_props(self):
        node = LeafNode(
            "a",
            "This is an anchor",
            {"href": "https://www.boot.dev", "class": "anchor"}
        )
        self.assertEqual(
            node.to_html(),
            "<a href=\"https://www.boot.dev\" class=\"anchor\">This is an anchor</a>"
        )

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello world")
        self.assertEqual(node.to_html(), "Hello world")

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_parent_node_recursive(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode("b", "Bold text")])
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b></p></div>"
        )


if __name__ == "__main__":
    unittest.main()
