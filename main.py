# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler

updater = Updater(token='1708564964:AAHCRsm_YKwlZ8aUExXp-pTqkSm7fA73ymw', use_context=True)
dispatcher = updater.dispatcher

FLAG_OFFSET = 127462 - ord('A')


def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + FLAG_OFFSET) + chr(ord(code[1]) + FLAG_OFFSET)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Zdarova, otsez!"+flag('uz')+flag('ru'))


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


if __name__ == '__main__':
    updater.start_polling()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
