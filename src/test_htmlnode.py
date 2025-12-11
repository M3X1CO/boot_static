import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(tag="a", props={"href": "https://google.com"})
        node2 = HTMLNode(tag="a", props={"href": "https://google.com", "target": "_blank"})
        node3 = HTMLNode(tag="p", props=None)

        assert node1.props_to_html() == ' href="https://google.com"'
        assert node2.props_to_html() == ' href="https://google.com" target="_blank"'
        assert node3.props_to_html() == ''

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        assert node.to_html() == "<p>Hello, world!</p>"

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        assert node.to_html() == '<a href="https://www.google.com">Click me!</a>'

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just text")
        assert node.to_html() == "Just text"

    def test_leaf_no_value_raises(self):
        try:
            LeafNode("p", None).to_html()
        except ValueError:
            pass
        else:
            assert False, "Expected ValueError"

if __name__ == "__main__":
    unittest.main()
