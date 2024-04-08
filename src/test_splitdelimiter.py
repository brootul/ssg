import unittest
from textnode import TextNode
from htmlnode import HTMLNode
from htmlnode import split_nodes_delimiter  # Replace 'your_module' with the actual module name where split_nodes_delimiter is defined

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        nodes = [TextNode("Here is `code` and more `code`", "text")]
        expected = [
            TextNode("Here is ", "text"),
            TextNode("code", "code"),
            TextNode(" and more ", "text"),
            TextNode("code", "code"),
            
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", "code"), expected)

    def test_split_bold(self):
        nodes = [TextNode("This is **bold** text", "text")]
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text"),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", "bold"), expected)

    def test_non_text_node(self):
        non_text_node = HTMLNode("div", [])
        nodes = [TextNode("Text before", "text"), non_text_node, TextNode("Text after", "text")]
        expected = [TextNode("Text before", "text"), non_text_node, TextNode("Text after", "text")]
        self.assertEqual(split_nodes_delimiter(nodes, "*", "italic"), expected)

    def test_unmatched_delimiter(self):
        nodes = [TextNode("This is *italic", "text")]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "*", "italic")

if __name__ == "__main__":
    unittest.main()
