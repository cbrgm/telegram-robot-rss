import unittest
import os
from util.database import DatabaseHandler


class TestDatabaseHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseHandler("resources/test.db")

    def test_add_user(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False)
        result = self.db.get_user(telegram_id=25525)

        self.assertEqual(result[0], 25525)
        self.assertEqual(result[1], "TestDummy")
        self.assertEqual(result[2], "John")
        self.assertEqual(result[3], "Snow")
        self.assertEqual(result[4], "DE")
        self.assertFalse(result[5])

    def test_remove_user(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False)
        self.db.remove_user(telegram_id=25525)
        result = self.db.get_user(telegram_id=25525)
        self.assertIsNone(result)

    def test_update_user(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False)
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
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False)
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

        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], "https://lorem-rss.herokuapp.com/feed")

    def test_remove_url(self):
        self.db.add_url(url="https://lorem-rss.herokuapp.com/feed")
        self.db.remove_url(url="https://lorem-rss.herokuapp.com/feed")
        result = self.db.get_url(url="https://lorem-rss.herokuapp.com/feed")
        self.assertIsNone(result)

    def test_update_url(self):
        self.db.add_url(url="https://lorem-rss.herokuapp.com/feed")
        entry = self.db.get_url(url="https://lorem-rss.herokuapp.com/feed")
        self.db.update_url(url_id=entry[0], url="https://google.com/")
        result = self.db.get_url(url="https://google.com/")
        self.assertEqual(result[1], "https://google.com/")

    def test_get_url(self):
        self.db.add_url(url="https://lorem-rss.herokuapp.com/feed")
        result = self.db.get_url(url="https://lorem-rss.herokuapp.com/feed")

        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], "https://lorem-rss.herokuapp.com/feed")

    def test_add_user_bookmark(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False)
        user = self.db.get_user(telegram_id=25525)

        self.db.add_user_bookmark(
            telegram_id=user[0], url="https://lorem-rss.herokuapp.com/feed01", alias="feed01")
        self.db.add_user_bookmark(
            telegram_id=user[0], url="https://lorem-rss.herokuapp.com/feed02", alias="feed02")
        self.db.add_user_bookmark(
            telegram_id=user[0], url="https://lorem-rss.herokuapp.com/feed03", alias="feed03")

    def test_get_urls_for_user(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False)
        user = self.db.get_user(telegram_id=25525)

        self.db.add_user_bookmark(
            telegram_id=user[0], url="https://lorem-rss.herokuapp.com/feed01", alias="feed01")
        self.db.add_user_bookmark(
            telegram_id=user[0], url="https://lorem-rss.herokuapp.com/feed02", alias="feed02")
        self.db.add_user_bookmark(
            telegram_id=user[0], url="https://lorem-rss.herokuapp.com/feed03", alias="feed03")

        result = self.db.get_urls_for_user(telegram_id=user[0])

        self.assertEqual(len(result), 3)
        self.assertEqual(
            result[0][1], "https://lorem-rss.herokuapp.com/feed01")
        self.assertEqual(
            result[1][1], "https://lorem-rss.herokuapp.com/feed02")
        self.assertEqual(
            result[2][1], "https://lorem-rss.herokuapp.com/feed03")

    def test_get_users_for_url(self):
        self.db.add_user(telegram_id=25526, username="TestDummy01",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False)
        self.db.add_user(telegram_id=25527, username="TestDummy02",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False)
        self.db.add_user(telegram_id=25528, username="TestDummy03",
                         firstname="John", lastname="Snow", language_code="DE", is_bot=False)

        self.db.add_user_bookmark(
            telegram_id=25526, url="http://cbrgm.de", alias="cbrgm")
        self.db.add_user_bookmark(
            telegram_id=25527, url="http://cbrgm.de", alias="niceblog")
        self.db.add_user_bookmark(
            telegram_id=25528, url="http://cbrgm.de", alias="awesome")
        url = self.db.get_url("http://cbrgm.de")
        result = self.db.get_users_for_url(url[0])

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][1], "TestDummy01")
        self.assertEqual(result[1][1], "TestDummy02")
        self.assertEqual(result[2][1], "TestDummy03")

    @classmethod
    def tearDownClass(cls):
        base_path = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(base_path, '..', "resources/test.db")
        os.remove(filepath)
