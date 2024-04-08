class TextNode:
    # Initialize the TextNode object with text, text_type, and an optional url
    def __init__(self, text, text_type, url=None):
        self.text = text  # The text content of the node
        self.text_type = text_type  # The type of text (e.g., "bold", "italic")
        self.url = url  # The URL if the text is a link or image; defaults to None

    # Equality comparison method to compare two TextNode objects
    def __eq__(self, other):
        # Ensure the other object is an instance of TextNode
        if not isinstance(other, TextNode):
            return NotImplemented
        # Compare text, text_type, and url properties of both objects
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    # Representation method to provide a string representation of the TextNode object
    def __repr__(self):
        # Returns a string in the format: TextNode(TEXT, TEXT_TYPE, URL)
        return f"TextNode({self.text!r}, {self.text_type!r}, {self.url!r})"