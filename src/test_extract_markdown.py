import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        text = "This is text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_links(self):
        text = "![image](https://example.com/img.png) and [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png")], matches)

    def test_extract_markdown_images_empty_alt(self):
        text = "This has an ![](https://example.com/img.png) empty alt"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/img.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_single(self):
        text = "This is text with a [link](https://www.example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_links_none(self):
        text = "This is text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_excludes_images(self):
        text = "This has a ![image](https://example.com/img.png) but no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_images(self):
        text = "![image](https://example.com/img.png) and [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_empty_text(self):
        text = "This has an [](https://example.com) empty link text"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)


if __name__ == "__main__":
    unittest.main()
