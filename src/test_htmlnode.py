import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_empty_props(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), '')

    def test_tag_only(self):
        node = HTMLNode(tag="p")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_no_tag(self):
        node = HTMLNode(value="text", props={"class": "text-class"})
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "text")
        self.assertEqual(node.props, {"class": "text-class"})

    def test_both_value_and_children(self):
        child = HTMLNode(tag="span", value="child")
        node = HTMLNode(tag="div", value="parent", children=[child])
        self.assertEqual(node.value, "parent")
        self.assertEqual(node.children, [child])

    def test_neither_value_nor_children(self):
        node = HTMLNode(tag="br")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])

    
# Add more tests as necessary

if __name__ == "__main__":
    unittest.main()
