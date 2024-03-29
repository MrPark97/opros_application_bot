#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging
import os

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackContext, MessageHandler, Filters

import answers
import language
import questions
import results
import phone_numbers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

START_MESSAGE = """
<b>Здравствуй, уважаемый друг!</b>

В целях поддержки малого и среднего бизнеса маленькая команда разработчиков работает над созданием мобильного приложения, где будут размещаться все скидки организациями сферы услуг, магазинов и общепита.
Наша цель узнать, хотел бы ты иметь такое приложение у себя в телефоне или нет, пройди небольшой опросник и помоги стартап-проекту!

------------------------------ Х ------------------------------

<b>Assalomu alaykum aziz do'stim!</b>

Kichik va o'rta biznesni qo'llab-quvvatlash maqsadida kichik dasturchilar guruhi xizmat ko'rsatish sohasidagi, do'konlardagi va umumiy ovqatlanishdagi tashkilotlarning barcha chegirma takliflarini joylashtirishi mumkin bo'lgan mobil ilovani yaratish ustida ishlamoqda.
Bizning maqsadimiz - sizning telefoningizda bunday dastur yuklash xohishi mavjudligini yoki yo'qligini aniqlash, qisqa so'rovnomadan o'ting va startap loyihaga yordam bering!
"""

LANGUAGE_MESSAGE = "Выберите язык / Tilni tanlang"
PHONE_MESSAGE_RU = "Укажите Ваш номер телефона или нажмите кнопку ниже, чтобы поделиться, или отправьте адрес своей электронной почты"
PHONE_MESSAGE_UZ = "Telefon raqamingizni kiriting yoki ulashish uchun quyidagi tugmani bosing, yoki elektron pochta manzilingizni yuboring"
FINISH_MESSAGE_RU = "Благодарим за пройденный опросник, ваше мнение очень ценно для нас!"
FINISH_MESSAGE_UZ = "So'rovnomani to'ldirganingiz uchun tashakkur, sizning fikringiz biz uchun juda qadrlidir!"

RU = 1
UZ = 2

START = 101
LANGUAGE = 102
PHONE_NUMBER = 103

FLAG_OFFSET = 127462 - ord('A')

ADMIN_LIST = [32640798, 199861356]


def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + FLAG_OFFSET) + chr(ord(code[1]) + FLAG_OFFSET)


def start(update: Update, _: CallbackContext) -> int:
    keyboard = [
        [
            KeyboardButton("НАЧАТЬ! / BOSHLAMOQ!"),
        ],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(START_MESSAGE, reply_markup=reply_markup, parse_mode='HTML')

    return START


def select_language(update: Update, _: CallbackContext) -> int:
    keyboard = [
        [
            KeyboardButton("Русский "+flag('ru'))
        ],
        [
            KeyboardButton("O`zbekcha "+flag('uz'))
        ],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(LANGUAGE_MESSAGE, reply_markup=reply_markup, parse_mode='HTML')

    return LANGUAGE


def questionnaire_1(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    question = questions.get_question_by_id(1)
    cur_answers = answers.get_answers_by_question(1)

    if update.message.text == "Русский "+flag('ru'):
        keyboard = [
            [
                KeyboardButton(cur_answers[0][1])
            ],
            [
                KeyboardButton(cur_answers[1][1])
            ],
            [
                KeyboardButton(cur_answers[2][1])
            ],
            [
                KeyboardButton(cur_answers[3][1])
            ],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        update.message.reply_text(
            question[1],
            reply_markup=reply_markup,
        )
        row_count = language.update_language(user.id, RU)
        if row_count == 0:
            language.insert_language(user.id, RU)

    elif update.message.text == "O`zbekcha "+flag('uz'):
        keyboard = [
            [
                KeyboardButton(cur_answers[0][2])
            ],
            [
                KeyboardButton(cur_answers[1][2])
            ],
            [
                KeyboardButton(cur_answers[2][2])
            ],
            [
                KeyboardButton(cur_answers[3][2])
            ],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        update.message.reply_text(
            question[2],
            reply_markup=reply_markup,
        )
        row_count = language.update_language(user.id, UZ)
        if row_count == 0:
            language.insert_language(user.id, UZ)

    return 1


def questionnaire_2(update: Update, _: CallbackContext) -> int:
    question_id = 2
    question_text = ""
    user = update.message.from_user
    question = questions.get_question_by_id(question_id)
    cur_answers = answers.get_answers_by_question(question_id)
    cur_language = language.get_language_by_user(user.id)[0]

    try:
        answer_id = answers.find_answer_id(question_id - 1, update.message.text)[0]
        results.insert_result(user.id, answer_id)
    except:
        pass

    if cur_language == RU:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][RU])
            ],
            [
                KeyboardButton(cur_answers[1][RU])
            ],
            [
                KeyboardButton(cur_answers[2][RU])
            ],
        ]

        question_text = question[RU]

    elif cur_language == UZ:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][UZ])
            ],
            [
                KeyboardButton(cur_answers[1][UZ])
            ],
            [
                KeyboardButton(cur_answers[2][UZ])
            ],
        ]

        question_text = question[UZ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(
        question_text,
        reply_markup=reply_markup,
    )
    return question_id


def questionnaire_3(update: Update, _: CallbackContext) -> int:
    question_id = 3
    question_text = ""
    user = update.message.from_user
    question = questions.get_question_by_id(question_id)
    cur_answers = answers.get_answers_by_question(question_id)
    cur_language = language.get_language_by_user(user.id)[0]

    try:
        answer_id = answers.find_answer_id(question_id - 1, update.message.text)[0]
        results.insert_result(user.id, answer_id)
    except:
        pass

    if cur_language == RU:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][RU])
            ],
            [
                KeyboardButton(cur_answers[1][RU])
            ],
        ]

        question_text = question[RU]

    elif cur_language == UZ:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][UZ])
            ],
            [
                KeyboardButton(cur_answers[1][UZ])
            ],
        ]

        question_text = question[UZ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(
        question_text,
        reply_markup=reply_markup,
    )
    return question_id


def questionnaire_4(update: Update, _: CallbackContext) -> int:
    question_id = 4
    question_text = ""
    user = update.message.from_user
    question = questions.get_question_by_id(question_id)
    cur_answers = answers.get_answers_by_question(question_id)
    cur_language = language.get_language_by_user(user.id)[0]

    try:
        answer_id = answers.find_answer_id(question_id - 1, update.message.text)[0]
        results.insert_result(user.id, answer_id)
    except:
        pass

    if cur_language == RU:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][RU])
            ],
            [
                KeyboardButton(cur_answers[1][RU])
            ],
        ]

        question_text = question[RU]

    elif cur_language == UZ:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][UZ])
            ],
            [
                KeyboardButton(cur_answers[1][UZ])
            ],
        ]

        question_text = question[UZ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(
        question_text,
        reply_markup=reply_markup,
    )
    return question_id


def questionnaire_5(update: Update, _: CallbackContext) -> int:
    question_id = 5
    question_text = ""
    user = update.message.from_user
    question = questions.get_question_by_id(question_id)
    cur_answers = answers.get_answers_by_question(question_id)
    cur_language = language.get_language_by_user(user.id)[0]

    try:
        answer_id = answers.find_answer_id(question_id - 1, update.message.text)[0]
        results.insert_result(user.id, answer_id)
    except:
        pass

    if cur_language == RU:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][RU])
            ],
            [
                KeyboardButton(cur_answers[1][RU])
            ],
        ]

        question_text = question[RU]

    elif cur_language == UZ:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][UZ])
            ],
            [
                KeyboardButton(cur_answers[1][UZ])
            ],
        ]

        question_text = question[UZ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(
        question_text,
        reply_markup=reply_markup,
    )
    return question_id


def questionnaire_6(update: Update, _: CallbackContext) -> int:
    question_id = 6
    question_text = ""
    user = update.message.from_user
    question = questions.get_question_by_id(question_id)
    cur_answers = answers.get_answers_by_question(question_id)
    cur_language = language.get_language_by_user(user.id)[0]

    try:
        answer_id = answers.find_answer_id(question_id - 1, update.message.text)[0]
        results.insert_result(user.id, answer_id)
    except:
        pass

    if cur_language == RU:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][RU])
            ],
            [
                KeyboardButton(cur_answers[1][RU])
            ],
        ]

        question_text = question[RU]

    elif cur_language == UZ:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][UZ])
            ],
            [
                KeyboardButton(cur_answers[1][UZ])
            ],
        ]

        question_text = question[UZ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(
        question_text,
        reply_markup=reply_markup,
    )
    return question_id


def questionnaire_7(update: Update, _: CallbackContext) -> int:
    question_id = 7
    question_text = ""
    user = update.message.from_user
    question = questions.get_question_by_id(question_id)
    cur_answers = answers.get_answers_by_question(question_id)
    cur_language = language.get_language_by_user(user.id)[0]

    try:
        answer_id = answers.find_answer_id(question_id - 1, update.message.text)[0]
        results.insert_result(user.id, answer_id)
    except:
        pass

    if cur_language == RU:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][RU])
            ],
            [
                KeyboardButton(cur_answers[1][RU])
            ],
            [
                KeyboardButton(cur_answers[2][RU])
            ],
            [
                KeyboardButton(cur_answers[3][RU])
            ],
            [
                KeyboardButton(cur_answers[4][RU])
            ],
            [
                KeyboardButton(cur_answers[5][RU])
            ],
        ]

        question_text = question[RU]

    elif cur_language == UZ:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][UZ])
            ],
            [
                KeyboardButton(cur_answers[1][UZ])
            ],
            [
                KeyboardButton(cur_answers[2][UZ])
            ],
            [
                KeyboardButton(cur_answers[3][UZ])
            ],
            [
                KeyboardButton(cur_answers[4][UZ])
            ],
            [
                KeyboardButton(cur_answers[5][UZ])
            ],
        ]

        question_text = question[UZ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(
        question_text,
        reply_markup=reply_markup,
    )
    return question_id


def questionnaire_8(update: Update, _: CallbackContext) -> int:
    question_id = 8
    question_text = ""
    user = update.message.from_user
    question = questions.get_question_by_id(question_id)
    cur_answers = answers.get_answers_by_question(question_id)
    cur_language = language.get_language_by_user(user.id)[0]

    try:
        answer_id = answers.find_answer_id(question_id - 1, update.message.text)[0]
        results.insert_result(user.id, answer_id)
    except:
        pass

    if cur_language == RU:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][RU])
            ],
            [
                KeyboardButton(cur_answers[1][RU])
            ],
        ]

        question_text = question[RU]

    elif cur_language == UZ:
        keyboard = [
            [
                KeyboardButton(cur_answers[0][UZ])
            ],
            [
                KeyboardButton(cur_answers[1][UZ])
            ],
        ]

        question_text = question[UZ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(
        question_text,
        reply_markup=reply_markup,
    )
    return question_id


def get_phone_number(update: Update, _: CallbackContext) -> int:
    question_text = ""
    user = update.message.from_user
    cur_language = language.get_language_by_user(user.id)[0]
    cur_answers = answers.get_answers_by_question(8)

    try:
        answer_id = answers.find_answer_id(8, update.message.text)[0]
        results.insert_result(user.id, answer_id)
    except:
        pass

    if update.message.text == cur_answers[1][RU] or update.message.text == cur_answers[1][UZ]:
        question_text = ""
        if cur_language == RU:
            question_text = FINISH_MESSAGE_RU
        elif cur_language == UZ:
            question_text = FINISH_MESSAGE_UZ
        update.message.reply_text(
            question_text, reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    if cur_language == RU:
        keyboard = [
            [
                KeyboardButton("📱 Отправить номер", request_contact=True)
            ],
            [
                KeyboardButton("❌ Отменить")
            ],
        ]

        question_text = PHONE_MESSAGE_RU

    elif cur_language == UZ:
        keyboard = [
            [
                KeyboardButton("📱 Raqamni yuboring", request_contact=True)
            ],
            [
                KeyboardButton("❌ Bekor qilish")
            ],
        ]

        question_text = PHONE_MESSAGE_UZ

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(
        question_text,
        reply_markup=reply_markup,
    )
    return PHONE_NUMBER


def finish(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    cur_language = language.get_language_by_user(user.id)[0]
    question_text = ""

    if update.message.contact is not None:
        phone_numbers.insert_phone_number(user.id, update.message.contact.phone_number)
    elif update.message.text is not None:
        if update.message.text != "❌ Bekor qilish" and update.message.text != "❌ Отменить":
            phone_numbers.insert_phone_number(user.id, update.message.text)

    if cur_language == RU:
        question_text = FINISH_MESSAGE_RU
    elif cur_language == UZ:
        question_text = FINISH_MESSAGE_UZ
    update.message.reply_text(
        question_text, reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Use /start to test this bot.")


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def statistics(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    if user.id not in ADMIN_LIST:
        update.message.reply_text(
            'Nice try)', reply_markup=ReplyKeyboardRemove()
        )
    else:
        result_string = "<b>Выбран язык:</b> \n"
        result_string += "Русский: "+str(language.get_language_by_type(RU)[0]) + "\n"
        result_string += "Узбекский: "+str(language.get_language_by_type(UZ)[0]) + "\n\n\n"

        all_questions = questions.get_all_questions()
        for question in all_questions:
            result_string += ("<b>"+question[1]+"</b>" + "\n")

            all_answers = answers.get_answers_by_question(question[0])
            for answer in all_answers:
                result_string += (answer[1]+": " + str(results.get_result_by_answer(answer[0])[0]) + "\n")

            result_string += "\n\n"

        result_string += ("<b>Количество уникальных респондентов: " +
                          str(results.get_unique_respondents_count()[0]) + "</b>\n")

        update.message.reply_text(
            result_string, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML'
        )


def contacts(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    if user.id not in ADMIN_LIST:
        update.message.reply_text(
            'Nice try)', reply_markup=ReplyKeyboardRemove()
        )
    else:
        result_string = "<b>Контакты:</b>\n\n"

        all_contacts = phone_numbers.get_all_contacts()
        for contact in all_contacts:
            result_string += (contact[2] + "\n")

        update.message.reply_text(
            result_string, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML'
        )


def main() -> None:
    # Port is given by Heroku
    PORT = int(os.environ.get('PORT', '8443'))
    TOKEN = "1708564964:AAHCRsm_YKwlZ8aUExXp-pTqkSm7fA73ymw"
    NAME = "opros_application_bot"

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('stat', statistics))
    updater.dispatcher.add_handler(CommandHandler('contacts', contacts))
    updater.dispatcher.add_handler(CommandHandler('cancel', cancel))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(Filters.text, select_language)],
            LANGUAGE: [MessageHandler(Filters.text, questionnaire_1)],
            1: [MessageHandler(Filters.text, questionnaire_2)],
            2: [MessageHandler(Filters.text, questionnaire_3)],
            3: [MessageHandler(Filters.text, questionnaire_4)],
            4: [MessageHandler(Filters.text, questionnaire_5)],
            5: [MessageHandler(Filters.text, questionnaire_6)],
            6: [MessageHandler(Filters.text, questionnaire_7)],
            7: [MessageHandler(Filters.text, questionnaire_8)],
            8: [MessageHandler(Filters.text, get_phone_number)],
            PHONE_NUMBER: [MessageHandler(Filters.text | Filters.contact, finish)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    updater.dispatcher.add_handler(conv_handler)

    # Start the Bot
    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://opros-application-bot.herokuapp.com/" + TOKEN)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
