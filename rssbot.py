# /bin/bash/python
# encoding: utf-8

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from util.filehandler import FileHandler
from util.datehandler import DateHandler
from util.threadpool import BatchThreadPool
from emoji import emojize
import feedparser
import re


class rssbot(object):

    def __init__(self):

        settings = FileHandler.load_json(path="resources/credentials.json")

        self.updater = Updater(settings["telegram_token"])
        self.dispatcher = self.updater.dispatcher

        # Add Commands to bot
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("stop", self.stop))
        self.dispatcher.add_handler(CommandHandler("help", self.help))
        self.dispatcher.add_handler(CommandHandler("list", self.list))
        self.dispatcher.add_handler(CommandHandler("about", self.about))
        self.dispatcher.add_handler(
            CommandHandler("add", self.add, pass_args=True))
        self.dispatcher.add_handler(
            CommandHandler("remove", self.remove, pass_args=True))
        # on noncommand i.e message - echo the message on Telegram
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.echo))

        # Start the Bot
        feed_updater = BatchThreadPool(
            update_interval=300, bot=self.dispatcher.bot)
        feed_updater.start()

        self.updater.start_polling()
        self.updater.idle()

    def start(self, bot, update):
        """Send a message when the command /start is issued."""

        if not FileHandler.file_exists("resources/userdata/" + str(update.message.from_user.id) + ".json"):
            message = "Hello! I don't think we've met before! I am an RSS News Bot and would like to help you to receive your favourite news in the future! Let me first set up a few things before we start..."
            update.message.reply_text(message)
            self.__setup_user_data(update)

        data = FileHandler.load_json(
            path="resources/userdata/" + str(update.message.from_user.id) + ".json")
        data["is_active"] = True
        FileHandler.save_json(data=data, path="resources/userdata/" +
                              str(update.message.from_user.id) + ".json")

        update.message.reply_text(
            emojize("You will now receive news! Use /help if you need some tips how to tell me what to do! :grin:", use_aliases=True))

    def add(self, bot, update, args):
        """Adds a rss subscription to user"""

        # Check if argument matches url format
        pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if pattern.match(args[0]) and len(args) == 2:

            data = FileHandler.load_json(
                path="resources/userdata/" + str(update.message.from_user.id) + ".json")

            if str(args[1]) not in data["subscriptions"]:
                new_item = {args[1]: args[0]}
                data["subscriptions"].update(new_item)
                FileHandler.save_json(
                    data=data, path="resources/userdata/" + str(update.message.from_user.id) + ".json")
                update.message.reply_text("I added " + str(
                    args[1]) + " to your subscriptions!")
            else:
                update.message.reply_text("Sorry! I already have an entry with name " +
                                          args[1] + " stored in your subscriptions.. Please choose another entry name or delete the entry using '/remove " + args[1] + "'")
        else:
            update.message.reply_text(
                "Sorry! I could not add the entry! Please use the the command passing the following arguments: /add <url> <entryname> \n\n Here is a short example: \n /add http://www.feedforall.com/sample.xml ExampleEntry")

    def remove(self, bot, update, args):
        """Removes an rss subscription from user"""

        if len(args) == 1:
            data = FileHandler.load_json(
                path="resources/userdata/" + str(update.message.from_user.id) + ".json")
            if args[0] in data["subscriptions"]:
                del data["subscriptions"][args[0]]
                update.message.reply_text(
                    "I removed " + args[0] + " from your subscriptions!")
                FileHandler.save_json(
                    data=data, path="resources/userdata/" + str(update.message.from_user.id) + ".json")
            else:
                update.message.reply_text(
                    "I can not find an entry with label " + args[0] + " in your subscriptions! Please check your subscriptions using /list and use the delete command again!")
        else:
            update.message.reply_text(
                "To remove a subscriptions from your list please use /remove <entryname>")

    def list(self, bot, update):
        """Displays a list of all user subscriptions"""
        update.message.reply_text(
            "Here is a list of all subscriptions I stored for you!")

        data = FileHandler.load_json(
            path="resources/userdata/" + str(update.message.from_user.id) + ".json")

        string = ""
        for key in data["subscriptions"]:
            string = string + \
                ("[" + key + "]\n " +
                 data["subscriptions"][key] + "\n\n")

        update.message.reply_text(string)

    def help(self, bot, update):
        """Send a message when the command /help is issued."""
        update.message.reply_text(
            'Here are all commands that are available to you: \n\n /add <url> <entryname> - Adds a new rss feed to your subscriptions \n /remove <entryname> - Removes an rss feed from your subscriptions \n /list - Displays a list of all subscriptions')

    def echo(self, bot, update):
        """Echo the user message."""
        update.message.reply_text(update.message.text)

    def stop(self, bot, update):
        """Stops the bot from working"""
        data = FileHandler.load_json(
            path="resources/userdata/" + str(update.message.from_user.id) + ".json")
        data["is_active"] = False
        FileHandler.save_json(data=data, path="resources/userdata/" +
                              str(update.message.from_user.id) + ".json")
        update.message.reply_text(
            "Oh.. Okay, I will not send you any more news updates! If you change your mind and you want to receive messages from me again use /start command again!")

    def about(self, bot, update):
        message = "Thank you for using <b>Blue RSS</b>! \n\n If you like the bot, please recommend it to others! \n\nDo you have problems, ideas or suggestions about what the bot should be able to do? Then contact my developer <a href='http://cbrgm.de'>@cbrgm</a> or create an issue on <a href='https://github.com/cbrgm/bluerss-telegrambot'>Github</a>. There you will also find my source code, if you are interested in how I work!"
        update.message.reply_text(message, parse_mode=ParseMode.HTML)

    def __setup_user_data(self, update):
        userdata = {}
        userdata["telegram_id"] = update.message.from_user.id
        userdata["username"] = update.message.from_user.username
        userdata["last_updated"] = str(DateHandler.get_datetime_now())
        userdata["is_active"] = True
        userdata["subscriptions"] = {}

        FileHandler.save_json(
            data=userdata, path="resources/userdata/" + str(update.message.from_user.id) + ".json")


if __name__ == '__main__':
    rssbot()
