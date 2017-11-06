import sqlite3
from util.filehandler import FileHandler as fh


class DatabaseHandler(object):

    def __init__(self, database_path):

        self.database_path = database_path

        if not fh.file_exists(self.database_path):
            sql_command = fh.load_file("resources/setup.sql")

            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            cursor.executescript(sql_command)
            conn.commit()
            conn.close()

    def add_user(self, telegram_id, username, firstname, lastname, language_code, is_bot):
        """Adds a user to sqlite database

        Args:
            param1 (int): The telegram_id of a user.
            param2 (str): The username of a user.
            param3 (str): The firstname of a user.
            param4 (str): The lastname of a user.
            param5 (str): The language_code of a user.
            param6 (str): The is_bot flag of a user.
        """

        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO user VALUES (?,?,?,?,?,?)",
                       (telegram_id, username, firstname, lastname, language_code, is_bot))

        conn.commit()
        conn.close()

    def remove_user(self, telegram_id):
        """Removes a user to sqlite database

        Args:
            param1 (int): The telegram_id of a user.
        """

        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM user WHERE telegram_id=" +
                       str(telegram_id))

        conn.commit()
        conn.close()

    def update_user(self, telegram_id, **kwargs):
        """Updates a user to sqlite database

        Args:
            param1 (int): The telegram_id of a user.
            param2 (kwargs): The attributes to be updated of a user.
        """

        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        sql_command = "UPDATE user SET "
        for key in kwargs:
            sql_command = sql_command + \
                str(key) + "='" + str(kwargs[key]) + "', "
        sql_command = sql_command[:-2] + \
            " WHERE telegram_id=" + str(telegram_id)

        cursor.execute(sql_command)

        conn.commit()
        conn.close()

    def get_user(self, telegram_id):
        """Returns a user by its id

        Args:
            param1 (int): The telegram_id of a user.

        Returns:
            list: The return value. A list containing all attributes of a user.
        """
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM user WHERE telegram_id = " + str(telegram_id))
        result = cursor.fetchone()

        conn.commit()
        conn.close()

        return result

    def add_url(self, url):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO web (url) VALUES (?)",
                       (url,))

        conn.commit()
        conn.close()

    def remove_url(self, url):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        sql_command = "DELETE FROM web WHERE url='" + str(url) + "';"

        cursor.execute(sql_command)

        conn.commit()
        conn.close()

    def update_url(self, url_id, **kwargs):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        sql_command = "UPDATE web SET "
        for key in kwargs:
            sql_command = sql_command + \
                str(key) + "='" + str(kwargs[key]) + "', "
        if len(kwargs) == 0:
            sql_command = sql_command + " WHERE url=" + str(url)
        else:
            sql_command = sql_command[:-2] + " WHERE url_id=" + str(url_id)

        cursor.execute(sql_command)

        conn.commit()
        conn.close()

    def get_url(self, url):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        sql_command = "SELECT * FROM web WHERE url='" + str(url) + "';"

        cursor.execute(sql_command)
        result = cursor.fetchone()

        conn.commit()
        conn.close()

        return result

    def add_user_bookmark(self, telegram_id, url, alias):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        self.add_url(url)  # add if not exists
        url_entry = self.get_url(url)

        cursor.execute("INSERT OR IGNORE INTO web_user VALUES (?,?,?)",
                       (url_entry[0], telegram_id, alias))

        conn.commit()
        conn.close()

    def get_urls_for_user(self, telegram_id):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT web.url_id, web.url, web_user.alias FROM web, web_user WHERE web_user.url_id = web.url_id AND web_user.telegram_id =" + str(telegram_id))

        result = cursor.fetchall()

        conn.commit()
        conn.close()

        return result

    def get_users_for_url(self, url_id):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT user.* FROM user, web_user WHERE web_user.telegram_id = user.telegram_id AND web_user.url_id =" + str(url_id))
        result = cursor.fetchall()

        conn.commit()
        conn.close()

        return result
