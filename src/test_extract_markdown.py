import unittest
from htmlnode import extract_markdown_images, extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "Text ![img1](http://example.com/img1.png) and ![img2](http://example.com/img2.png)"
        expected = [("img1", "http://example.com/img1.png"), ("img2", "http://example.com/img2.png")]
        self.assertEqual(extract_markdown_images(text), expected)

        # Test with no images
        text_no_images = "Text with no images."
        self.assertEqual(extract_markdown_images(text_no_images), [])

    def test_extract_markdown_links(self):
        text = "Text [link1](http://example.com) and [link2](http://example.com/link2)"
        expected = [("link1", "http://example.com"), ("link2", "http://example.com/link2")]
        self.assertEqual(extract_markdown_links(text), expected)

        # Test with no links
        text_no_links = "Text with no links."
        self.assertEqual(extract_markdown_links(text_no_links), [])

if __name__ == '__main__':
    unittest.main()


