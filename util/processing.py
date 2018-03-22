# /bin/bash/python/

from telegram.error import (TelegramError, Unauthorized)
from telegram import ParseMode
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread as RunningThread
from util.datehandler import DateHandler
from util.database import DatabaseHandler
from util.feedhandler import FeedHandler
import datetime
import threading
import traceback
from time import sleep


class BatchProcess(threading.Thread):

    def __init__(self, database, update_interval, bot):
        RunningThread.__init__(self)
        self.db = database
        self.update_interval = float(update_interval)
        self.bot = bot
        self.running = True

    def run(self):
        """
        Starts the BatchThreadPool
        """

        while self.running:
            # Init workload queue, add queue to ThreadPool
            url_queue = self.db.get_all_urls()
            self.parse_parallel(queue=url_queue, threads=4)

            # Sleep for interval
            sleep(self.update_interval)

    def parse_parallel(self, queue, threads):
        time_started = datetime.datetime.now()

        pool = ThreadPool(threads)
        pool.map(self.update_feed, queue)
        pool.close()
        pool.join()

        time_ended = datetime.datetime.now()
        duration = time_ended - time_started
        print("Finished updating! Parsed " + str(len(queue)) +
              " rss feeds in " + str(duration) + " !")

    def update_feed(self, url):
        telegram_users = self.db.get_users_for_url(url=url[0])

        for user in telegram_users:
            if user[6]:  # is_active
                try:
                    for post in FeedHandler.parse_feed(url[0]):
                        self.send_newest_messages(
                            url=url, post=post, user=user)
                except:
                    traceback.print_exc()
                    message = "Something went wrong when I tried to parse the URL: \n\n " + \
                        url[0] + "\n\nCould you please check that for me? Remove the url from your subscriptions using the /remove command, it seems like it does not work anymore!"
                    self.bot.send_message(
                        chat_id=user[0], text=message, parse_mode=ParseMode.HTML)

        self.db.update_url(url=url[0], last_updated=str(
            DateHandler.get_datetime_now()))

    def send_newest_messages(self, url, post, user):
        post_update_date = DateHandler.parse_datetime(datetime=post.updated)
        url_update_date = DateHandler.parse_datetime(datetime=url[1])

        if post_update_date > url_update_date:
            message = "[" + user[7] + "] <a href='" + post.link + \
                "'>" + post.title + "</a>"
            try:
                self.bot.send_message(
                    chat_id=user[0], text=message, parse_mode=ParseMode.HTML)
            except Unauthorized:
                self.db.update_user(telegram_id=user[0], is_active=0)
            except TelegramError:
                # handle all other telegram related errors
                pass

    def set_running(self, running):
        self.running = running
