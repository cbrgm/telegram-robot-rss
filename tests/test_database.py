import unittest
from util.database import DatabaseHandler


class TestDatabaseHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        self.db = DatabaseHandler("resources/test.db")

    def test_add_user(self):
        self.db.add_user(telegram_id=25525, username="TestDummy",
                         firstname="First", lastname="Last", language_code="DE", is_bot=False)
        result = self.get_user(telegram_id=25525)
        assertEqual(result[0], 25525)

    @classmethod
    def tearDownClass(cls):
