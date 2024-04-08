import unittest
from htmlnode import markdown_to_blocks  # Adjust import based on your file structure

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_blocks(self):
        markdown = "Block 1\n\nBlock 2\n\nBlock 3"
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_blocks_with_internal_newlines(self):
        markdown = "Block 1 line 1\nBlock 1 line 2\n\nBlock 2"
        expected = ["Block 1 line 1\nBlock 1 line 2", "Block 2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_blocks_with_excessive_newlines(self):
        markdown = "\n\n\nBlock 1\n\n\n\nBlock 2\n\n\n"
        expected = ["Block 1", "Block 2"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_input(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_no_blocks(self):
        markdown = "\n\n\n"
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_features(self):
        markdown = "**Bold**\n\n*Italic*\n\n`Code`"
        expected = ["**Bold**", "*Italic*", "`Code`"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

# Run the tests
if __name__ == '__main__':
    unittest.main()
