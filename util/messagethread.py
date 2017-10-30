# /bin/bash/python/
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram import ParseMode
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread
from util.filehandler import FileHandler
from util.datehandler import DateHandler
from dateutil import parser as DateParser
import feedparser
import threading
import datetime
from time import sleep


class MessageThread(threading.Thread):

    def __init__(self, update_interval, bot):
        Thread.__init__(self)
        self.update_interval = update_interval
        self.running = True
        self.bot = bot

    def run(self):
        """Starts the MessageThread"""
        while self.running:
            file_queue = FileHandler.get_files_in_dir(
                path="resources/userdata")
            self.parse_parallel(queue=file_queue, threads=4)
            sleep(self.update_interval)

    def parse_parallel(self, queue, threads):
        print("Updating rss feeds of " + str(len(queue)) +
              " files... Using ThreadPool, " + str(threads) + " Threads available!")
        time_started = datetime.datetime.now()

        pool = ThreadPool(threads)
        pool.map(self.update_feed, queue)
        pool.close()
        pool.join()

        time_ended = datetime.datetime.now()
        duration = time_ended - time_started
        print("Finished task in " + str(duration) + " !")

    def update_feed(self, filename):
        data = FileHandler.load_json(
            "resources/userdata/" + filename)

        if data["is_active"]:
            for subscription_url in data["subscriptions"].values():
                newsfeed = feedparser.parse(subscription_url)
                for post in newsfeed.entries[0:10]:
                    self.send_newest_messages(
                        feed_post=post, user_data=data, filename=filename)

        data["last_updated"] = str(DateHandler.get_datetime_now())
        FileHandler.save_json(
            data=data, path="resources/userdata/" + filename)

    def send_newest_messages(self, feed_post, user_data, filename):
        post_update_date = DateParser.parse(feed_post.updated)
        userfile_update_date = DateParser.parse(user_data["last_updated"])

        if post_update_date > userfile_update_date:
            message = "<a href='" + feed_post.link + \
                "'>" + feed_post.title + "</a>"
            try:
                self.bot.send_message(
                    chat_id=user_data["telegram_id"], text=message, parse_mode=ParseMode.HTML)
            except Unauthorized:
                print("Test")
                user_data["is_active"] = False
                FileHandler.save_json(
                    data=user_data, path="resources/userdata/" + filename)
            except BadRequest:
                # handle malformed requests - read more below!
                pass
            except TimedOut:
                # handle slow connection problems
                pass
            except NetworkError:
                # handle other connection problems
                pass
            except ChatMigrated as e:
                # the chat_id of a group has changed, use e.new_chat_id instead
                pass
            except TelegramError:
                # handle all other telegram related errors
                pass

    def set_running(self, running):
        self.running = running
