import unittest
from htmlnode import markdown_to_html_node, HTMLNode  # Ensure correct import based on your project structure

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_convert_heading(self):
        markdown = "# Heading 1"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, "<div><h1>Heading 1</h1></div>")

    def test_convert_paragraph(self):
        markdown = "This is a paragraph."
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, "<div><p>This is a paragraph.</p></div>")

    def test_convert_code(self):
        markdown = "```\nCode block\n```"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, "<div><pre><code>Code block</code></pre></div>")

    def test_convert_blockquote(self):
        markdown = "> This is a quote"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, "<div><blockquote>This is a quote</blockquote></div>")

    def test_convert_unordered_list(self):
        markdown = "* Item 1\n* Item 2"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>")

    def test_convert_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, "<div><ol><li>Item 1</li><li>Item 2</li></ol></div>")

    def test_full_document(self):
        markdown = (
        "# Heading 1\n\n"
        "This is a paragraph.\n\n"
        "> This is a quote\n\n"
        "* Item 1\n"
        "* Item 2\n\n"
        "1. Item 1\n"
        "2. Item 2\n\n"
        "```\n"
        "Code block\n"
        "```"
    )
        expected_html = "<div><h1>Heading 1</h1><p>This is a paragraph.</p><blockquote>This is a quote</blockquote><ul><li>Item 1</li><li>Item 2</li></ul><ol><li>Item 1</li><li>Item 2</li></ol><pre><code>Code block</code></pre></div>"
        result = markdown_to_html_node(markdown).to_html()
        self.assertEqual(result, expected_html)
    

