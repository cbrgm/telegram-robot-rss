import unittest
from util.feedhandler import FeedHandler


class TestFeedHandler(unittest.TestCase):

    def test_parse_feed(self):
        url = "https://lorem-rss.herokuapp.com/feed"
        feed = FeedHandler.parse_feed(url)
        self.assertIsNotNone(url)
        url = "https://lorem-rss.herokuapp.com/feed"

    def test_parse_feed_amount(self):
        url = "https://lorem-rss.herokuapp.com/feed"
        feed = FeedHandler.parse_feed(url, 5)
        self.assertIsNotNone(url)
        self.assertEqual(len(feed), 5)

    def test_is_parsable(self):
        url = "https://lorem-rss.herokuapp.com/feed"
        self.assertTrue(FeedHandler.is_parsable(url))
        url = "https://google.de"
        self.assertFalse(FeedHandler.is_parsable(url))
        url = "www.google.de"
        self.assertFalse(FeedHandler.is_parsable(url))

    def test_format_url_string(self):
        url = "https://lorem-rss.herokuapp.com/feed"
        url = FeedHandler.format_url_string(url)
        self.assertEqual(url, "https://lorem-rss.herokuapp.com/feed")

        url = "www.lorem-rss.herokuapp.com/feed"
        url = FeedHandler.format_url_string(url)
        self.assertEqual(url, "http://www.lorem-rss.herokuapp.com/feed")

        url = "lorem-rss.herokuapp.com/feed"
        url = FeedHandler.format_url_string(url)
        self.assertEqual(url, "http://lorem-rss.herokuapp.com/feed")
