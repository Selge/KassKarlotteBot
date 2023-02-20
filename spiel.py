import telebot
from telebot import types
import random

import key
import spielmaterial as sm


bot = telebot.TeleBot(key.get_key())

item = {}
gameIsStart = False
game_won = False
game_lost = False


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Start game")
    markup.add(button)

    if message.text == "/start":
        bot.send_message(message.chat.id, sm.message().format(message.from_user, bot.get_me()),
                         parse_mode='html',
                         reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):
    if message.chat.type == 'private':
        if message.text == "Start game":
            global gameIsStart
            gameIsStart = True
        else:
            bot.send_message(message.chat.id, "use /start to play!")

    if gameIsStart == True:
        item = {}
        bot.send_message(message.chat.id, "The hunt is started")
        global markup
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(0, 9):
            item[i] = types.InlineKeyboardButton(sm.board[i], callback_data=str(i))
        markup.row(item[0], item[1], item[2])
        markup.row(item[3], item[4], item[5])
        markup.row(item[6], item[7], item[8])
        bot.send_message(message.chat.id, "Choose a cell", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callbackInline(call):
    if (call.message):
        randomCell = random.randint(0, 9)
        if sm.board[randomCell] == sm.player_sign:
            randomCell = random.randint(0, 9)
        if sm.board[randomCell] == sm.computer_sign:
            randomCell = random.randint(0, 9)
        if sm.board[randomCell] == " ":
            sm.board[randomCell] = sm.computer_sign
        # player manager
        for i in range(9):
            if call.data == str(i):
                if (sm.board[i] == " "):
                    sm.board[i] = sm.player_sign

            item[i] = types.InlineKeyboardButton(sm.board[i], callback_data=str(i))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Catch all rats!',
                              reply_markup=None)
        # update cells
        global markup
        markup.row(item[0], item[1], item[2])
        markup.row(item[3], item[4], item[5])
        markup.row(item[6], item[7], item[8])

        bot.send_message(call.message.chat.id, "Choose a cell", reply_markup=markup)
        global game_won
        if game_won:
            bot.send_message(call.message.chat.id, "All the rats are in a new bag! 😸")
            game_won = True
            gameIsStart = False
        global game_lost
        if game_lost:
            bot.send_message(call.message.chat.id, "All the rats ran away! 😿")
            game_lost = True
            gameIsStart = False


bot.polling(none_stop=True)
