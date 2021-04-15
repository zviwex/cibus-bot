#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.
import subprocess
from datetime import time
import pytz
import sys
"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import telegram
from telegram import Update, ForceReply, bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
users = []

def run(command):
    return subprocess.check_output(command, shell=True)

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        )
    update.message.reply_markdown_v2(
        fr'Lets save your creds to cibus',
        )
    update.message.reply_markdown_v2(
        fr'Note that is REALLY\!\!\! unsafe, do it only if you don\'t give a shit about your password',
        )

    update.message.reply_markdown_v2(
        'enter /cred [username\(email\)] [password]',
        reply_markup=ForceReply(selective=True),
    )

    def callback_alarm(context: telegram.ext.CallbackContext):
        context.bot.send_message(context.job.context, text='Hi This is a daily reminder')
        idx = -1
        for user in users:
            if user[0] == id:
                break

        _, username, password = user
        
        run(f"curl 'https://www.mysodexo.co.il/' -H 'Connection: keep-alive' -H 'Origin: https://www.mysodexo.co.il'  -H 'Content-Type: application/x-www-form-urlencoded'   -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'   -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'   -H 'Referer: https://www.mysodexo.co.il/'   --data-raw '__VIEWSTATE=S7Vca9h0ihqiy4m0asl2ybYgednoCBRZ9t%2Br%2B4Fjm6fePg%2B8BdflxxYWKMLkgZDBM7U6HVq5hwV3NcGHFHEJmdqsslRS8%2FezSInY7pBkOw0JsVgyNU8z5MweyY3Ip7549HoRXfP9OOMwVT3KaO7tAimfsdd2z%2FXlJ%2Fi3Z2kYlJ00xrWeOebc40Z4aLFYhwFZPROR%2FFY%2FEhOlHcu9wKGn1clIc5v3UHhbwDZSQdBWe%2F15giWp5R%2B530U8IBSar9VJyEYvf4dXhfmgkb8%2Bsml5U1n0yEONmgbz6YyNpT930WqnFBrNpe%2FxvwcD3Bo%2BTC9SbCeXzijvcqVFjTt%2B4F%2FbDveDmvtWmq4JnxMkcfqFzH0QSxGVJcnfPnN7bVX4MSMmnXOOSw%3D%3D&__VIEWSTATEGENERATOR=E12A6B22&txtUsr={username}&txtPas={password}&ctl12=&txtPhone=&g-recaptcha-response=&ctl19='   --compressed   --cookie-jar /tmp/cookie")
        state = run("curl 'https://www.mysodexo.co.il/new_ajax_service.aspx?getBdgt=1'  --cookie /tmp/cookie")
        run('Rm /tmp/cookie')
        context.bot.send_message(context.job.context, text=f"You have left {state.decode('utf8')} shekels")
    chat_id = update.message.chat_id
        

    update.message.reply_markdown_v2('Daily reminder has been set\! You\'ll get notified at 10:30 AM daily')
    context.job_queue.run_daily(callback_alarm,context=chat_id, name=str(chat_id),days=(0, 1, 2, 3, 4, 5, 6),time = time(hour = 10, minute = 30, second = 50, tzinfo=pytz.timezone('Asia/Jerusalem')))

def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def cred_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    _, username, password = update.message.text.split()
    user = update.effective_user
    users.append([user.id, username, password])
    update.message.reply_text('Cred added!')


def stop_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    uid = update.effective_user.id
    idx = -1
    for i, user in enumerate(users):
        if user[0] == uid:
            idx = i
            break
    
    users.remove(users[i])
    update.message.reply_text('Removed')

def budget_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    uid = update.effective_user.id
    idx = -1
    for user in users:
        if user[0] == uid:
            break

    _, username, password = user
    
    run(f"curl 'https://www.mysodexo.co.il/' -H 'Connection: keep-alive' -H 'Origin: https://www.mysodexo.co.il'  -H 'Content-Type: application/x-www-form-urlencoded'   -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'   -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'   -H 'Referer: https://www.mysodexo.co.il/'   --data-raw '__VIEWSTATE=S7Vca9h0ihqiy4m0asl2ybYgednoCBRZ9t%2Br%2B4Fjm6fePg%2B8BdflxxYWKMLkgZDBM7U6HVq5hwV3NcGHFHEJmdqsslRS8%2FezSInY7pBkOw0JsVgyNU8z5MweyY3Ip7549HoRXfP9OOMwVT3KaO7tAimfsdd2z%2FXlJ%2Fi3Z2kYlJ00xrWeOebc40Z4aLFYhwFZPROR%2FFY%2FEhOlHcu9wKGn1clIc5v3UHhbwDZSQdBWe%2F15giWp5R%2B530U8IBSar9VJyEYvf4dXhfmgkb8%2Bsml5U1n0yEONmgbz6YyNpT930WqnFBrNpe%2FxvwcD3Bo%2BTC9SbCeXzijvcqVFjTt%2B4F%2FbDveDmvtWmq4JnxMkcfqFzH0QSxGVJcnfPnN7bVX4MSMmnXOOSw%3D%3D&__VIEWSTATEGENERATOR=E12A6B22&txtUsr={username}&txtPas={password}&ctl12=&txtPhone=&g-recaptcha-response=&ctl19='   --compressed   --cookie-jar /tmp/cookie")
    state = run("curl 'https://www.mysodexo.co.il/new_ajax_service.aspx?getBdgt=1'  --cookie /tmp/cookie")
    run('Rm /tmp/cookie')
    update.message.reply_text(f"You have left {state.decode('utf8')} shekels")


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(sys.argv[1])
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("cred", cred_command))
    dispatcher.add_handler(CommandHandler("stop", stop_command))
    dispatcher.add_handler(CommandHandler("budget", budget_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()




if __name__ == '__main__':
    main()