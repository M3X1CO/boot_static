import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, extract_title


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_simple(self):
        md = "# Heading\n\nParagraph text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "Paragraph text"])

    def test_markdown_to_blocks_multiple_paragraphs(self):
        md = "First paragraph\n\nSecond paragraph\n\nThird paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["First paragraph", "Second paragraph", "Third paragraph"]
        )

    def test_markdown_to_blocks_with_whitespace(self):
        md = "  # Heading  \n\n  Paragraph with spaces  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "Paragraph with spaces"])

    def test_markdown_to_blocks_excessive_newlines(self):
        md = "First block\n\n\n\nSecond block\n\n\n\n\nThird block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block", "Third block"])

    def test_markdown_to_blocks_single_block(self):
        md = "Just one block of text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block of text"])

    def test_markdown_to_blocks_heading_and_list(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_code_block(self):
        md = """Here's some code:

```python
def hello():
    print("world")
```

And more text"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here's some code:",
                '```python\ndef hello():\n    print("world")\n```',
                "And more text",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nof text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h2(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h3(self):
        block = "### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h4(self):
        block = "#### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h5(self):
        block = "##### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_invalid_no_space(self):
        block = "#This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_invalid_too_many_hashes(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ncode here\nmore code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_language(self):
        block = "```python\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_invalid_no_closing(self):
        block = "```\ncode here\nno closing backticks"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_single_line(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multiline(self):
        block = ">This is a quote\n>with multiple lines\n>of text"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_invalid_missing_line(self):
        block = ">This is a quote\nthis line is not\n>back to quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_single_item(self):
        block = "- Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple_items(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid_no_space(self):
        block = "-Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_invalid_missing_line(self):
        block = "- Item 1\nNot a list item\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_single_item(self):
        block = "1. Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_items(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_wrong_number(self):
        block = "1. Item 1\n3. Item 3\n4. Item 4"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_starts_at_zero(self):
        block = "0. Item 0\n1. Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_starts_at_two(self):
        block = "2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_no_space(self):
        block = "1.Item 1\n2.Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello"
        title = extract_title(markdown)
        self.assertEqual(title, "Hello")

    def test_extract_title_with_whitespace(self):
        markdown = "#  Hello World  "
        title = extract_title(markdown)
        self.assertEqual(title, "Hello World")

    def test_extract_title_with_content(self):
        markdown = """# My Title

This is some content.

## Heading 2

More content here."""
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")

    def test_extract_title_with_leading_newlines(self):
        markdown = """

# The Title

Content here."""
        title = extract_title(markdown)
        self.assertEqual(title, "The Title")

    def test_extract_title_no_h1(self):
        markdown = """## Heading 2

This has no h1."""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))

    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_only_h2(self):
        markdown = "## Not an h1"
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
