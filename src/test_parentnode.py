import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_basic_parent_node(self):
        child = LeafNode("span", "Child")
        node = ParentNode("div", [child])
        self.assertEqual(node.to_html(), "<div><span>Child</span></div>")

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "Child")])

    def test_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_nested_parent_nodes(self):
        inner_child = LeafNode("span", "Inner Child")
        inner_node = ParentNode("div", [inner_child])
        outer_node = ParentNode("section", [inner_node])
        self.assertEqual(outer_node.to_html(), "<section><div><span>Inner Child</span></div></section>")

    def test_mixed_nesting(self):
        leaf1 = LeafNode("span", "Leaf 1")
        leaf2 = LeafNode("span", "Leaf 2")
        inner_node = ParentNode("div", [leaf1, leaf2])
        leaf3 = LeafNode("span", "Leaf 3")
        outer_node = ParentNode("section", [inner_node, leaf3])
        self.assertEqual(outer_node.to_html(), "<section><div><span>Leaf 1</span><span>Leaf 2</span></div><span>Leaf 3</span></section>")

    def test_deep_nesting(self):
        level3 = LeafNode("span", "Deep")
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("section", [level2])
        self.assertEqual(level1.to_html(), "<section><div><span>Deep</span></div></section>")

    def test_props_handling(self):
        node = ParentNode("a", [LeafNode(None, "Click here")], {"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Click here</a>')

if __name__ == "__main__":
    unittest.main()
