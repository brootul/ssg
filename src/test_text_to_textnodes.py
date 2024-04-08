import unittest
from htmlnode import TextNode, text_to_textnodes  # Adjust import based on your file structure

class TestTextToTextNodes(unittest.TestCase):
    def test_mixed_markdown_features(self):
        text = "This is **bold** with an *italic* word, a `code block`, an ![image](https://example.com/image.png), and a [link](https://example.com)"
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word, a ", "text"),
            TextNode("code block", "code"),
            TextNode(", an ", "text"),
            TextNode("image", "image", "https://example.com/image.png"),
            TextNode(", and a ", "text"),
            TextNode("link", "link", "https://example.com"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_only(self):
        text = "Just some plain text."
        expected = [TextNode("Just some plain text.", "text")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold_only(self):
        text = "**Bold only**"
        expected = [TextNode("Bold only", "bold")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic_only(self):
        text = "*Italic only*"
        expected = [TextNode("Italic only", "italic")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code_only(self):
        text = "`Code only`"
        expected = [TextNode("Code only", "code")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image_only(self):
        text = "![Image](https://example.com/image.png)"
        expected = [TextNode("Image", "image", "https://example.com/image.png")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link_only(self):
        text = "[Link](https://example.com)"
        expected = [TextNode("Link", "link", "https://example.com")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_empty_text(self):
        text = ""
        expected = []
        self.assertEqual(text_to_textnodes(text), expected)

    def test_no_markdown(self):
        text = "This text has no Markdown syntax."
        expected = [TextNode("This text has no Markdown syntax.", "text")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_nested_markdown(self):
        text = "Some **bold and *italic* text** here."
        expected = [
            TextNode("Some ", "text"),
            TextNode("bold and *italic* text", "bold"),
            TextNode(" here.", "text"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)


# Run the tests
if __name__ == '__main__':
    unittest.main()
