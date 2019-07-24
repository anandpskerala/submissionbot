import re
import os
import json
import sys
import signal
import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction, ParseMode
from datetime import datetime, timedelta
from time import sleep
import logging
import requests

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

currentPID = os.getpid()
if 'pid' not in os.listdir():
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
else:
    with open('pid', mode='r') as f:
        try:
            os.kill(int(f.read()), signal.SIGTERM)
            print("Terminating previous instance of " +
                  os.path.realpath(__file__))
        except ProcessLookupError:
            subprocess.run(['rm', 'pid'])
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)

bot_token = "xyz"
channel_id = "xyz"

updater = Updater(bot_token)
dispatcher = updater.dispatcher

botdetails = {}

print("Ready to rock!..!!")


def start(bot, update):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text='''
Hi! I'm here to help you publish your intresting bot idea on channel, send /submit or /help.'''
    )


def help(bot, update):
    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.sendMessage(chat_id=update.message.chat_id, text='''HELP ME!''')


def submitbot(bot, update):
    global botdetails

    bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING)
    botdetails[update.message.chat_id] = []
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text='''
After your submission the bot will be displayed on channel''')
    bot.sendMessage(
        chat_id=update.message.chat_id, text='''What's the title for Bot''')


def details(bot, update):
    global botdetails

    if update.message != None and update.message.chat_id in botdetails.keys():
        if len(botdetails[update.message.chat_id]) == 0:
            botdetails[update.message.chat_id].append(update.message.text)
            bot.sendMessage(
                chat_id=update.message.chat_id,
                text='''Enter the description for bot:''')
        elif len(botdetails[update.message.chat_id]) == 1:
            botdetails[update.message.chat_id].append(update.message.text)
            bot.sendMessage(
                chat_id=update.message.chat_id,
                text='''Send link related to bot:''')
        elif len(botdetails[update.message.chat_id]) == 2:
            if re.match(
                    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                    update.message.text):
                botdetails[update.message.chat_id].append(update.message.text)
                bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text=
                    '''Tell me about it's use cases seprately in multiple lines.'''
                )
            else:
                bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text='''Enter a valid link!''')
        elif len(botdetails[update.message.chat_id]) == 3:
            if re.match(r"(.*?)", update.message.text):
                botdetails[update.message.chat_id].append(update.message.text)
                use_cases = '''{}'''.format(
                    botdetails[update.message.chat_id][3])
                lines = use_cases.split('\n')
                for i in range(len(lines)):
                    lines[i] = '● ' + lines[i]
                use_cases = '\n'.join(lines)
                bot.sendMessage(
                    chat_id=channel_id,
                    text='''⏩ *{}*'''.format(
                        botdetails[update.message.chat_id][0]) + '''\n\n''' +
                    botdetails[update.message.chat_id][1] + '''\n''' +
                    botdetails[update.message.chat_id][2] +
                    '''\n\n👥 *Use-Cases:* \n\n''' + use_cases,
                    parse_mode=ParseMode.MARKDOWN)
                    
                bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text='''⏩ *{}*'''.format(
                        botdetails[update.message.chat_id][0]) + '''\n\n''' +
                    botdetails[update.message.chat_id][1] + '''\n''' +
                    botdetails[update.message.chat_id][2] +
                    '''\n\n👥 *Use-Cases:* \n\n''' + use_cases,
                    parse_mode=ParseMode.MARKDOWN)
                bot.sendMessage(
                    chat_id=update.message.chat_id,
                    text='''Your bot idea has been posted to channel''')
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text=''':)''')
    elif update.message.chat.type == 'private':
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='''Please use /submit to submit bots''')


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('submit', submitbot))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.text, details))

updater.start_polling()
