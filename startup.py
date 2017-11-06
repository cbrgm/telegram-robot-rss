from util.database import DatabaseHandler


def main():
    db = DatabaseHandler("resources/sample.db")
    db.add_user(telegram_id=25525, username="TestDummy",
                firstname="First", lastname="Last", language_code="DE", is_bot=False)
    result = db.get_user(telegram_id=25525)
    print(result[0])

    db.update_user(telegram_id=25525, username="Test", is_bot=False)


if __name__ == '__main__':
    main()
