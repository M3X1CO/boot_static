import unittest
from inline_markdown import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_image_at_end(self):
        node = TextNode(
            "Text followed by ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("Text with ![img1](https://url1.com)", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("More text with ![img2](https://url2.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "https://url1.com"),
                TextNode("Bold text", TextType.BOLD),
                TextNode("More text with ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "https://url2.com"),
            ],
            new_nodes,
        )

    def test_split_images_non_text_nodes(self):
        node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_single(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_link_at_start(self):
        node = TextNode(
            "[link](https://www.example.com) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_at_end(self):
        node = TextNode(
            "Text followed by [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("Text with [link1](https://url1.com)", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("More text with [link2](https://url2.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://url1.com"),
                TextNode("Bold text", TextType.BOLD),
                TextNode("More text with ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://url2.com"),
            ],
            new_nodes,
        )

    def test_split_links_non_text_nodes(self):
        node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_with_images(self):
        node = TextNode(
            "Text with ![image](https://img.com) and [link](https://link.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Should only split the link, not the image
        self.assertListEqual(
            [
                TextNode("Text with ![image](https://img.com) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://link.com"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
