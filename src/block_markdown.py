from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    """
    Split a markdown document into blocks.
    
    Blocks are separated by blank lines (double newlines).
    Leading/trailing whitespace is stripped from each block.
    Empty blocks are removed.
    
    Args:
        markdown: A string containing the full markdown document
        
    Returns:
        A list of block strings
        
    Example:
        markdown = "# Heading\\n\\nParagraph text\\n\\n- List item"
        returns ["# Heading", "Paragraph text", "- List item"]
    """
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Args:
        block: A string containing a single markdown block (already stripped)
        
    Returns:
        A BlockType enum value
        
    Block type rules:
    - Headings: Start with 1-6 # characters, followed by a space
    - Code: Start with ``` and end with ```
    - Quote: Every line starts with >
    - Unordered list: Every line starts with "- " (dash + space)
    - Ordered list: Every line starts with number + ". " starting at 1
    - Paragraph: Everything else
    """
    lines = block.split("\n")
    
    # Check for heading (1-6 # characters followed by a space)
    if block.startswith("#"):
        # Count the number of # characters at the start
        hash_count = 0
        for char in block:
            if char == "#":
                hash_count += 1
            else:
                break
        # Valid heading: 1-6 hashes followed by a space
        if 1 <= hash_count <= 6 and len(block) > hash_count and block[hash_count] == " ":
            return BlockType.HEADING
    
    # Check for code block (starts and ends with ```)
    if len(lines) > 1 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if block.startswith(">"):
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if block.startswith("- "):
        is_unordered_list = True
        for line in lines:
            if not line.startswith("- "):
                is_unordered_list = False
                break
        if is_unordered_list:
            return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with 1. 2. 3. etc.)
    if block.startswith("1. "):
        is_ordered_list = True
        for i, line in enumerate(lines):
            expected_prefix = f"{i + 1}. "
            if not line.startswith(expected_prefix):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH


def text_to_children(text):
    """
    Convert inline markdown text to a list of HTMLNode children.
    
    This processes all inline markdown (bold, italic, code, links, images)
    and returns HTMLNode objects ready to be children of a block element.
    
    Args:
        text: A string containing inline markdown
        
    Returns:
        A list of HTMLNode objects (LeafNodes)
    """
    # Start with a single text node
    text_nodes = [TextNode(text, TextType.TEXT)]
    
    # Process each type of inline markdown in order
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    
    # Convert TextNodes to HTMLNodes
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    return html_nodes


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    lines = block.split("\n")
    paragraph_text = " ".join(lines)
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    # Count the number of # characters
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    if level < 1 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")
    
    # Extract the text after the hashes and space
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    # Remove the opening and closing ```
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    
    # Extract the code content (remove ``` from start and end)
    code_content = block[3:-3]
    
    # Remove leading newline if present
    if code_content.startswith("\n"):
        code_content = code_content[1:]
    
    # If there's a language specifier on the first line, remove it
    lines = code_content.split("\n", 1)
    if lines[0] and " " not in lines[0] and len(lines[0]) < 20:
        # First line looks like a language specifier
        code_content = lines[1] if len(lines) > 1 else ""
    
    # Don't process inline markdown in code blocks
    code_node = LeafNode("code", code_content)
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    lines = block.split("\n")
    # Remove the > from each line
    quote_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        quote_lines.append(line[1:].strip())
    
    quote_text = " ".join(quote_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        if not line.startswith("- "):
            raise ValueError("Invalid unordered list")
        # Remove the "- " prefix
        text = line[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            raise ValueError("Invalid ordered list")
        # Remove the number prefix
        text = line[len(expected_prefix):]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    
    return ParentNode("ol", list_items)


def block_to_html_node(block):
    """
    Convert a single markdown block to an HTMLNode.
    
    Args:
        block: A string containing a single markdown block
        
    Returns:
        An HTMLNode (ParentNode) representing the block
    """
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document to an HTMLNode.
    
    Args:
        markdown: A string containing the full markdown document
        
    Returns:
        A ParentNode with tag "div" containing all the block HTMLNodes
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    
    return ParentNode("div", children)


def extract_title(markdown):
    """
    Extract the h1 header from a markdown document.
    
    Args:
        markdown: A string containing markdown text
        
    Returns:
        The h1 header text (without the # and whitespace)
        
    Raises:
        Exception: If no h1 header is found
    """
    lines = markdown.split("\n")
    
    for line in lines:
        line = line.strip()
        if line.startswith("# ") and not line.startswith("## "):
            # Found an h1 header
            return line[2:].strip()
    
    raise Exception("No h1 header found in markdown")
