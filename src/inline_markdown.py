import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    """
    Extract markdown images from text.
    Returns a list of tuples: (alt_text, url)
    
    Example:
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        returns [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract markdown links from text (excluding images).
    Returns a list of tuples: (anchor_text, url)
    
    Example:
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        returns [("to boot dev", "https://www.boot.dev")]
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    """
    Split TextNodes containing markdown images into separate nodes.
    
    Example:
        node = TextNode("Text with ![alt](url)", TextType.TEXT)
        returns [
            TextNode("Text with ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url")
        ]
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        
        for image_alt, image_url in images:
            sections = original_text.split(f"![{image_alt}]({image_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextNodes containing markdown links into separate nodes.
    
    Example:
        node = TextNode("Text with [anchor](url)", TextType.TEXT)
        returns [
            TextNode("Text with ", TextType.TEXT),
            TextNode("anchor", TextType.LINK, "url")
        ]
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        for link_anchor, link_url in links:
            sections = original_text.split(f"[{link_anchor}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link_anchor, TextType.LINK, link_url))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    
    return new_nodes
