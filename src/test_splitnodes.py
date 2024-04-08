import unittest
from htmlnode import TextNode, split_nodes_image

class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        nodes = [TextNode("![alt](url)", "text")]
        expected = [TextNode("alt", "image", "url")]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_image_with_text(self):
        nodes = [TextNode("Text before ![alt](url) text after", "text")]
        expected = [
            TextNode("Text before ", "text"),
            TextNode("alt", "image", "url"),
            TextNode(" text after", "text"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_multiple_images(self):
        nodes = [TextNode("![alt1](url1)![alt2](url2)", "text")]
        expected = [
            TextNode("alt1", "image", "url1"),
            TextNode("alt2", "image", "url2"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_no_image(self):
        nodes = [TextNode("No image here", "text")]
        self.assertEqual(split_nodes_image(nodes), nodes)

    def test_non_text_node(self):
        non_text_node = TextNode("Non-text", "code")
        self.assertEqual(split_nodes_image([non_text_node]), [non_text_node])

if __name__ == '__main__':
    unittest.main()


from htmlnode import split_nodes_link

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        nodes = [TextNode("[text](url)", "text")]
        expected = [TextNode("text", "link", "url")]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_link_with_text(self):
        nodes = [TextNode("Text before [text](url) text after", "text")]
        expected = [
            TextNode("Text before ", "text"),
            TextNode("text", "link", "url"),
            TextNode(" text after", "text"),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_multiple_links(self):
        nodes = [TextNode("[text1](url1)[text2](url2)", "text")]
        expected = [
            TextNode("text1", "link", "url1"),
            TextNode("text2", "link", "url2"),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_no_link(self):
        nodes = [TextNode("No link here", "text")]
        self.assertEqual(split_nodes_link(nodes), nodes)

    def test_non_text_node(self):
        non_text_node = TextNode("Non-text", "code")
        self.assertEqual(split_nodes_link([non_text_node]), [non_text_node])

if __name__ == '__main__':
    unittest.main()
