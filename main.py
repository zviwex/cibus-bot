#!/usr/local/bin/python3
from datetime import time
import pytz
import sys
import cibus
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import dynamodb
import secret


def start(update: Update, context: CallbackContext) -> None:
    'Send a message when the command /start is issued.'
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
    )
    update.message.reply_markdown_v2(
        fr'Lets save your creds to cibus',
    )

    # Sience this is a POC, the implementation is not includes a secure way 
    # to pass the credentialas.
    # If you're interested in such feature please open an issue on github
    update.message.reply_markdown_v2(
        fr'Note that is REALLY\!\!\! unsafe, do it only if you don\'t give a shit about your password',
    )

    update.message.reply_markdown_v2(
        'enter /cred [username\(email\)] [password]',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    'Send a message when the command /help is issued.'
    update.message.reply_text('Help!')


def get_balance(userid):
    user = dynamodb.get_user(str(userid))
    username, password = user['mail'], user['password']

    return cibus.get_balance(username, secret.decrypt_password(password))


def callback_alarm(context: telegram.ext.CallbackContext):
    for user in dynamodb.get_users():
        userid = user['userid']
        context.bot.send_message(userid, text='Hi This is a daily reminder')

        context.bot.send_message(
            userid, text=f"You have left {get_balance(userid)} shekels")


def cred_command(update: Update, context: CallbackContext) -> None:
    'Send a message when the command /help is issued.'
    _, username, password = update.message.text.split()
    user = str(update.effective_user.id)

    dynamodb.put_user(user, username, secret.encrypt_password(password))

    update.message.reply_text('Cred added!')
    update.message.reply_markdown_v2(
        'Daily reminder has been set\! You\'ll get notified at 10:30 AM daily')


def stop_command(update: Update, _: CallbackContext) -> None:
    'Send a message when the command /help is issued.'
    uid = str(update.effective_user.id)

    dynamodb.delete_user(uid)

    update.message.reply_text('Removed')


def budget_command(update: Update, _: CallbackContext) -> None:
    'Send a message when the command /help is issued.'
    userid = str(update.effective_user.id)

    update.message.reply_text(f"You have left {get_balance(userid)} shekels")


def echo(update: Update, _: CallbackContext) -> None:
    'Echo the user message.'
    update.message.reply_text("What?")


def set_watch(updater):
    updater.job_queue.run_daily(callback_alarm, name='allusers', days=(0, 1, 2, 3, 4, 5, 6), time=time(
        hour=10, minute=30, second=00, tzinfo=pytz.timezone('Asia/Jerusalem')))


def main() -> None:
    'Start the bot.'
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
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    set_watch(updater)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
