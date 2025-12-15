import unittest
from block_markdown import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

    def test_headings_multiple_levels(self):
        md = """
# Heading 1

## Heading 2

### Heading 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_heading_with_inline_markdown(self):
        md = "## This is a **bold** heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is a <b>bold</b> heading</h2></div>")

    def test_quote(self):
        md = ">This is a quote\n>with multiple lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><blockquote>This is a quote with multiple lines</blockquote></div>"
        )

    def test_quote_with_inline_markdown(self):
        md = ">This is a **bold** quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><blockquote>This is a <b>bold</b> quote</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_unordered_list_with_inline_markdown(self):
        md = """
- **Bold** item
- _Italic_ item
- `Code` item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>Bold</b> item</li><li><i>Italic</i> item</li><li><code>Code</code> item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        md = """
1. **Bold** item
2. _Italic_ item
3. `Code` item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>Bold</b> item</li><li><i>Italic</i> item</li><li><code>Code</code> item</li></ol></div>",
        )

    def test_paragraph_with_link(self):
        md = "This is a paragraph with a [link](https://example.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with a <a href="https://example.com">link</a></p></div>',
        )

    def test_paragraph_with_image(self):
        md = "This is a paragraph with an ![image](https://example.com/img.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with an <img src="https://example.com/img.png" alt="image"></p></div>',
        )

    def test_complex_document(self):
        md = """
# Welcome

This is a **complex** document with _multiple_ types of `content`.

## Features

Here are some features:

- **Bold** text
- _Italic_ text
- `Code` snippets

## Code Example

```
def hello():
    print("world")
```

> This is a quote about the code

1. First thing
2. Second thing
3. Third thing
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Just verify it doesn't crash and contains key elements
        self.assertIn("<h1>Welcome</h1>", html)
        self.assertIn("<h2>Features</h2>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<pre><code>", html)
        self.assertIn("<blockquote>", html)
        self.assertIn("<ol>", html)

    def test_code_block_with_language(self):
        md = """
```python
def hello():
    print("world")
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><pre><code>def hello():\n    print("world")\n</code></pre></div>',
        )


if __name__ == "__main__":
    unittest.main()
