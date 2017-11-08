import unittest
import os
from util.database import DatabaseHandler
from util.datehandler import DateHandler as dh


class TestDatabaseHandler(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseHandler("resources/test.db")

    def test_add_user(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)
        result = self.db.get_user(telegram_id=25525)

        self.assertEqual(result[0], 25525)
        self.assertEqual(result[1], "TestDummy")
        self.assertEqual(result[2], "John")
        self.assertEqual(result[3], "Snow")
        self.assertEqual(result[4], "DE")
        self.assertFalse(result[5])
        self.assertTrue(result[6])

    def test_remove_user(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)
        self.db.remove_user(telegram_id=25525)
        result = self.db.get_user(telegram_id=25525)
        self.assertIsNone(result)

    def test_update_user(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)
        self.db.update_user(telegram_id=25525,
                            firstname="Jonathan", is_bot=True)
        result = self.db.get_user(telegram_id=25525)
        self.assertEqual(result[0], 25525)
        self.assertEqual(result[1], "TestDummy")
        self.assertEqual(result[2], "Jonathan")
        self.assertEqual(result[3], "Snow")
        self.assertEqual(result[4], "DE")
        self.assertTrue(result[5])

    def test_get_user(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)
        result = self.db.get_user(telegram_id=25525)

        self.assertEqual(result[0], 25525)
        self.assertEqual(result[1], "TestDummy")
        self.assertEqual(result[2], "John")
        self.assertEqual(result[3], "Snow")
        self.assertEqual(result[4], "DE")
        self.assertFalse(result[5])

    def test_add_url(self):
        self.db.add_url(url="https://lorem-rss.herokuapp.com/feed")
        result = self.db.get_url(url="https://lorem-rss.herokuapp.com/feed")

        self.assertEqual(result[0], "https://lorem-rss.herokuapp.com/feed")

    def test_remove_url(self):
        self.db.add_url(url="https://lorem-rss.herokuapp.com/feed")
        self.db.remove_url(url="https://lorem-rss.herokuapp.com/feed")
        result = self.db.get_url(url="https://lorem-rss.herokuapp.com/feed")
        self.assertIsNone(result)

    def test_remove_url_has_references(self):
        self.db.add_url(url="https://lorem-rss.herokuapp.com/feed")

        self.db.add_user(telegram_id=25525, username="TestDummy01",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)
        self.db.add_user(telegram_id=25526, username="TestDummy02",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)

        self.db.add_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed", alias="Test")
        self.db.add_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed", alias="TestEntry")

        self.db.remove_url(url="https://lorem-rss.herokuapp.com/feed")

        result = self.db.get_users_for_url(
            url="https://lorem-rss.herokuapp.com/feed")
        self.assertEqual(len(result), 0)

        result = self.db.get_url(url="https://lorem-rss.herokuapp.com/feed")
        self.assertIsNone(result)

    def test_update_url(self):
        self.db.add_url(url="https://lorem-rss.herokuapp.com/feed")
        entry = self.db.get_url(url="https://lorem-rss.herokuapp.com/feed")

        timestamp = str(dh.get_datetime_now())

        self.db.update_url(
            url="https://lorem-rss.herokuapp.com/feed", last_updated=timestamp)
        result = self.db.get_url(url="https://lorem-rss.herokuapp.com/feed")
        self.assertEqual(result[1], timestamp)

    def test_get_url(self):
        self.db.add_url(url="https://lorem-rss.herokuapp.com/feed")
        result = self.db.get_url(url="https://lorem-rss.herokuapp.com/feed")

        self.assertEqual(result[0], "https://lorem-rss.herokuapp.com/feed")

    def test_add_user_bookmark(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)

        self.db.add_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed01", alias="feed01")
        self.db.add_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed02", alias="feed02")
        self.db.add_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed03", alias="feed03")

        result = self.db.get_urls_for_user(telegram_id=25525)

        self.assertEqual(len(result), 3)
        self.assertEqual(
            result[0][0], "https://lorem-rss.herokuapp.com/feed01")
        self.assertEqual(
            result[1][0], "https://lorem-rss.herokuapp.com/feed02")
        self.assertEqual(
            result[2][0], "https://lorem-rss.herokuapp.com/feed03")

    def test_remove_bookmark(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)

        self.db.add_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed01", alias="feed")

        self.db.remove_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed01")
        result = self.db.get_urls_for_user(telegram_id=25525)
        self.assertEqual(len(result), 0)

    def test_update_bookmark(self):
        pass

    def test_get_urls_for_user(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)

        self.db.add_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed01", alias="feed01")
        self.db.add_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed02", alias="feed02")
        self.db.add_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed03", alias="feed03")

        result = self.db.get_urls_for_user(telegram_id=25525)

        self.assertEqual(len(result), 3)
        self.assertEqual(
            result[0][0], "https://lorem-rss.herokuapp.com/feed01")
        self.assertEqual(
            result[1][0], "https://lorem-rss.herokuapp.com/feed02")
        self.assertEqual(
            result[2][0], "https://lorem-rss.herokuapp.com/feed03")

    def test_get_users_for_url(self):
        self.db.add_user(telegram_id=25526, username="TestDummy01",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)
        self.db.add_user(telegram_id=25527, username="TestDummy02",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)
        self.db.add_user(telegram_id=25528, username="TestDummy03",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)

        self.db.add_user_bookmark(
            telegram_id=25526, url="http://cbrgm.de", alias="cbrgm")
        self.db.add_user_bookmark(
            telegram_id=25527, url="http://cbrgm.de", alias="niceblog")
        self.db.add_user_bookmark(
            telegram_id=25528, url="http://cbrgm.de", alias="awesome")

        result = self.db.get_users_for_url("http://cbrgm.de")

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][1], "TestDummy01")
        self.assertEqual(result[1][1], "TestDummy02")
        self.assertEqual(result[2][1], "TestDummy03")

    def test_get_user_bookmark(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)
        self.db.add_user_bookmark(
            url="https://lorem-rss.herokuapp.com/feed", telegram_id=25525, alias="Test")

        bookmark = self.db.get_user_bookmark(telegram_id=25525, alias="Test")
        self.assertEqual(bookmark[0], "https://lorem-rss.herokuapp.com/feed")
        self.assertEqual(bookmark[1], "Test")

    def test_remove_if_not_referenced(self):
        self.db.add_url(url="https://lorem-rss.herokuapp.com/feed")
        self.db.add_user(telegram_id=25525, username="TestDummy01",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)

        self.db.add_user_bookmark(
            url="https://lorem-rss.herokuapp.com/feed", telegram_id=25525, alias="Test")

        self.db.remove_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed")

        web = self.db.get_url("https://lorem-rss.herokuapp.com/feed")
        self.assertIsNone(web)

    def test_dont_remove_if_referenced(self):
        self.db.add_url(url="https://lorem-rss.herokuapp.com/feed")
        self.db.add_user(telegram_id=25525, username="TestDummy01",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)
        self.db.add_user(telegram_id=25526, username="TestDummy02",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False, is_active=True)
        self.db.add_user_bookmark(
            url="https://lorem-rss.herokuapp.com/feed", telegram_id=25525, alias="Test")
        self.db.add_user_bookmark(
            url="https://lorem-rss.herokuapp.com/feed", telegram_id=25526, alias="MyTest")

        self.db.remove_user_bookmark(
            telegram_id=25525, url="https://lorem-rss.herokuapp.com/feed")

        web = self.db.get_url("https://lorem-rss.herokuapp.com/feed")
        self.assertEqual(web[0], "https://lorem-rss.herokuapp.com/feed")

    def tearDown(self):
        base_path = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(base_path, '..', "resources/test.db")
        os.remove(filepath)
