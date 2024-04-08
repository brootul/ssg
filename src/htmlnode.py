class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ''
        return ' ' + ' '.join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"


from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode requires a value")
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("ParentNode requires a tag")
        if not children:
            raise ValueError("ParentNode requires children")
        super().__init__(tag, None, children, props)

    def to_html(self):
        children_html = ''.join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'

from htmlnode import LeafNode
from textnode import TextNode

def text_node_to_html_node(text_node):
    # Define the mapping from text_type to HTML tag
    text_type_to_tag = {
        "text": None,
        "bold": "b",
        "italic": "i",
        "code": "code",
        "link": "a",
        "image": "img",
    }

    # Check if the text_node's type is one of the expected types
    if text_node.text_type not in text_type_to_tag:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")

    # Get the corresponding HTML tag for the text type
    tag = text_type_to_tag[text_node.text_type]

    # Handle specific cases based on text_type
    if text_node.text_type == "link":
        # Ensure URL is provided for links
        if not text_node.url:
            raise ValueError("URL is required for link text type")
        return LeafNode(tag, text_node.text, {"href": text_node.url})

    elif text_node.text_type == "image":
        # Ensure URL is provided for images
        if not text_node.url:
            raise ValueError("URL is required for image text type")
        # Use text as alt text for the image
        return LeafNode(tag, "", {"src": text_node.url, "alt": text_node.text})

    else:
        # For other types, create a LeafNode with the tag and text
        return LeafNode(tag, text_node.text)

# Example usage
text_node = TextNode("Click me!", "link", "https://www.example.com")
html_node = text_node_to_html_node(text_node)
print(html_node.to_html())  # Outputs: <a href="https://www.example.com">Click me!</a>


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # Only split text type TextNode objects
        if isinstance(node, TextNode) and node.text_type == "text":
            parts = node.text.split(delimiter)
            # If a closing delimiter is not found, raise an exception
            if len(parts) % 2 == 0:
                raise ValueError(f"Unmatched delimiter '{delimiter}' found.")
            
            # Alternating between the original text type and the new text type
            for i, part in enumerate(parts):
                if part or i != len(parts) - 1:  # Avoid adding empty nodes unless they are in the middle
                    new_type = text_type if i % 2 == 1 else "text"
                    new_nodes.append(TextNode(part, new_type))
        else:
            # For non-text type nodes, add them to the new list as-is
            new_nodes.append(node)
    return new_nodes


import re

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches  # Returns a list of tuples (alt text, URL)

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches  # Returns a list of tuples (anchor text, URL)


#Splits the TextNode's
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == "text":
            images = extract_markdown_images(node.text)
            if not images:
                new_nodes.append(node)
                continue
            
            start = 0
            for alt_text, url in images:
                end = node.text.find(f"![{alt_text}]({url})", start)
                # Text before the image
                if end > start:
                    new_nodes.append(TextNode(node.text[start:end], "text"))
                # The image itself
                new_nodes.append(TextNode(alt_text, "image", url))
                start = end + len(f"![{alt_text}]({url})")
            
            # Text after the last image
            if start < len(node.text):
                new_nodes.append(TextNode(node.text[start:], "text"))
        else:
            new_nodes.append(node)
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == "text":
            links = extract_markdown_links(node.text)
            if not links:
                new_nodes.append(node)
                continue

            last_index = 0
            for anchor_text, url in links:
                # Splitting at the first occurrence of the link markdown
                prefix, _, suffix = node.text[last_index:].partition(f"[{anchor_text}]({url})")
                
                # Add the text before the link if it's not empty
                if prefix:
                    new_nodes.append(TextNode(prefix, "text"))
                
                # Add the link node
                new_nodes.append(TextNode(anchor_text, "link", url))

                # Update the last index to skip over the current link in the next iteration
                last_index += len(prefix) + len(anchor_text) + len(url) + 4  # 4 accounts for the brackets and parentheses

            # Handle any remaining text after the last link
            if last_index < len(node.text):
                new_nodes.append(TextNode(node.text[last_index:], "text"))
        else:
            # For non-text nodes, add them to the new list as-is
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    
    # Split for bold text
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    
    # Split for italic text
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    
    # Split for code blocks
    nodes = split_nodes_delimiter(nodes, "`", "code")
    
    # Split for images
    nodes = split_nodes_image(nodes)
    
    # Split for links
    nodes = split_nodes_link(nodes)
    
    # Filter out any empty nodes that might have been created
    nodes = [node for node in nodes if node.text]
    
    return nodes


def markdown_to_blocks(markdown):
    # Normalize the input by replacing CRLF with LF (if present)
    normalized_markdown = markdown.replace('\r\n', '\n')

    # Split the markdown text where there are two or more consecutive newlines.
    blocks = re.split(r'\n\n+', normalized_markdown)

    # Trim leading and trailing whitespace from each block
    blocks = [block.strip() for block in blocks if block.strip()]

    return blocks


import re

# Define block type constants
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UNORDERED_LIST = "unordered_list"
BLOCK_TYPE_ORDERED_LIST = "ordered_list"
BLOCK_TYPE_PARAGRAPH = "paragraph"

def block_to_block_type(block):
    # Check for heading
    if re.match(r'^#{1,6} ', block):
        return BLOCK_TYPE_HEADING

    # Check for code block
    if block.startswith('```') and block.endswith('```'):
        return BLOCK_TYPE_CODE

    # Check for quote block
    if all(line.startswith('>') for line in block.split('\n')):
        return BLOCK_TYPE_QUOTE

    # Check for unordered list block
    if all(re.match(r'^(\*|-) ', line) for line in block.split('\n')):
        return BLOCK_TYPE_UNORDERED_LIST

    # Check for ordered list block
    if all(re.match(r'^\d+\. ', line) for line in block.split('\n')):
        return BLOCK_TYPE_ORDERED_LIST

    # If none of the above, it's a paragraph
    return BLOCK_TYPE_PARAGRAPH


class HTMLNode:
    def __init__(self, tag, children=None, text=None, props=None):
        self.tag = tag
        self.children = children if children is not None else []
        self.text = text
        self.props = props if props is not None else {}

    def to_html(self):
        # Convert the node and its children to HTML
        # This is a simplified version. You'll need to expand it based on the node's content and children
        if self.tag:
            start_tag = f"<{self.tag}{self.props_to_html()}>"
            end_tag = f"</{self.tag}>"
        else:
            start_tag = end_tag = ""

        inner_html = self.text or "".join(child.to_html() for child in self.children)
        return f"{start_tag}{inner_html}{end_tag}"

    def props_to_html(self):
        # Convert props to HTML attributes
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

def convert_heading(block):
    level = block.count('#')
    return HTMLNode(f"h{level}", text=block.strip('# '))

def convert_paragraph(block):
    return HTMLNode("p", text=block)

def convert_code(block):
    # Assuming the first and last line are the backticks
    code_content = "\n".join(block.split('\n')[1:-1])
    return HTMLNode("pre", children=[HTMLNode("code", text=code_content)])

def convert_blockquote(block):
    return HTMLNode("blockquote", text=block.strip('> '))

def convert_list(block, ordered=False):
    items = block.split('\n')
    list_tag = "ol" if ordered else "ul"
    list_items = [HTMLNode("li", text=item.strip('*- ').strip('0123456789. ')) for item in items]
    return HTMLNode(list_tag, children=list_items)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div_children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BLOCK_TYPE_HEADING:
            div_children.append(convert_heading(block))
        elif block_type == BLOCK_TYPE_PARAGRAPH:
            div_children.append(convert_paragraph(block))
        elif block_type == BLOCK_TYPE_CODE:
            div_children.append(convert_code(block))
        elif block_type == BLOCK_TYPE_QUOTE:
            div_children.append(convert_blockquote(block))
        elif block_type == BLOCK_TYPE_UNORDERED_LIST:
            div_children.append(convert_list(block))
        elif block_type == BLOCK_TYPE_ORDERED_LIST:
            div_children.append(convert_list(block, ordered=True))

    return HTMLNode("div", children=div_children)

# In htmlnode.py

def extract_title(markdown):
    """
    Extracts the h1 header from the markdown content.

    :param markdown: Markdown content as a string
    :return: The text of the first h1 header
    :raises: Exception if no h1 header is found
    """
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line.strip('# ').strip()
    raise Exception("No h1 header found in the markdown content.")
