import unittest
from htmlnode import block_to_block_type, BLOCK_TYPE_HEADING, BLOCK_TYPE_CODE, BLOCK_TYPE_QUOTE, BLOCK_TYPE_UNORDERED_LIST, BLOCK_TYPE_ORDERED_LIST, BLOCK_TYPE_PARAGRAPH

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BLOCK_TYPE_HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BLOCK_TYPE_HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BLOCK_TYPE_HEADING)

    def test_code_block(self):
        code_block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(code_block), BLOCK_TYPE_CODE)

    def test_quote_block(self):
        quote_block = "> This is a quote"
        self.assertEqual(block_to_block_type(quote_block), BLOCK_TYPE_QUOTE)

    def test_unordered_list(self):
        unordered_list_block = "* Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(unordered_list_block), BLOCK_TYPE_UNORDERED_LIST)
        unordered_list_block_with_dash = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(unordered_list_block_with_dash), BLOCK_TYPE_UNORDERED_LIST)

    def test_ordered_list(self):
        ordered_list_block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(ordered_list_block), BLOCK_TYPE_ORDERED_LIST)

    def test_paragraph(self):
        paragraph = "This is a paragraph."
        self.assertEqual(block_to_block_type(paragraph), BLOCK_TYPE_PARAGRAPH)

    def test_mixed_content(self):
        # This should be recognized as a paragraph since it doesn't meet the specific criteria of other types
        mixed_content = "This is a paragraph with a list:\n- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(mixed_content), BLOCK_TYPE_PARAGRAPH)

if __name__ == '__main__':
    unittest.main()
