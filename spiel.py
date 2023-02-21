import telebot
from telebot import types
import random

import key
import spielmaterial as sm


robot = telebot.TeleBot(key.get_key())

game_started = False
game_won = False
game_lost = False


@robot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Start game")
    markup.add(button)

    if message.text == "/start":
        robot.send_message(message.chat.id, sm.message().format(message.from_user, robot.get_me()),
                           parse_mode='html',
                           reply_markup=markup)


@robot.message_handler(content_types=['text'])
def new_game(message):
    if message.chat.type == 'private':
        if message.text == "Start game":
            global gameIsStart
            gameIsStart = True
        else:
            robot.send_message(message.chat.id, "use /start to play")

    if gameIsStart == True:
        empty_cell = {}
        robot.send_message(message.chat.id, "The hunt is started")
        global markup
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(0, 9):
            empty_cell[i] = types.InlineKeyboardButton(sm.gameboard[i], callback_data=str(i))
        markup.row(empty_cell[0], empty_cell[1], empty_cell[2])
        markup.row(empty_cell[3], empty_cell[4], empty_cell[5])
        markup.row(empty_cell[6], empty_cell[7], empty_cell[8])
        robot.send_message(message.chat.id, "Choose a cell to catch a rat!", reply_markup=markup)


@robot.callback_query_handler(func=lambda call: True)
def playing(call):
    if (call.message):
        move = random.randint(0, 9)
        if sm.gameboard[move] == sm.player_sign:
            move = random.randint(0, 9)
        if sm.gameboard[move] == sm.robot_sign:
            move = random.randint(0, 9)
        if sm.gameboard[move] == " ":
            sm.gameboard[move] = sm.robot_sign

        for i in range(9):
            if call.data == str(i):
                if (sm.gameboard[i] == " "):
                    sm.gameboard[i] = sm.player_sign

            sm.winner(sm.gameboard[0], sm.gameboard[1], sm.gameboard[2])
            sm.winner(sm.gameboard[0], sm.gameboard[4], sm.gameboard[8])
            sm.winner(sm.gameboard[2], sm.gameboard[4], sm.gameboard[6])
            sm.winner(sm.gameboard[3], sm.gameboard[4], sm.gameboard[5])
            sm.winner(sm.gameboard[6], sm.gameboard[7], sm.gameboard[8])
            sm.winner(sm.gameboard[0], sm.gameboard[3], sm.gameboard[6])
            sm.winner(sm.gameboard[1], sm.gameboard[4], sm.gameboard[7])
            sm.winner(sm.gameboard[2], sm.gameboard[5], sm.gameboard[8])
            sm.loser(sm.gameboard[0], sm.gameboard[1], sm.gameboard[2])
            sm.loser(sm.gameboard[0], sm.gameboard[4], sm.gameboard[8])
            sm.loser(sm.gameboard[2], sm.gameboard[4], sm.gameboard[6])
            sm.loser(sm.gameboard[3], sm.gameboard[4], sm.gameboard[5])
            sm.loser(sm.gameboard[6], sm.gameboard[7], sm.gameboard[8])
            sm.loser(sm.gameboard[0], sm.gameboard[3], sm.gameboard[6])
            sm.loser(sm.gameboard[1], sm.gameboard[4], sm.gameboard[7])
            sm.loser(sm.gameboard[2], sm.gameboard[5], sm.gameboard[8])

            sm.game_cell[i] = types.InlineKeyboardButton(sm.gameboard[i], callback_data=str(i))

        robot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Catch all the rats!',
                                reply_markup=None)
        global markup
        markup.row(sm.game_cell[0], sm.game_cell[1], sm.game_cell[2])
        markup.row(sm.game_cell[3], sm.game_cell[4], sm.game_cell[5])
        markup.row(sm.game_cell[6], sm.game_cell[7], sm.game_cell[8])

        robot.send_message(call.message.chat.id, "Choose a cell to catch a rat!", reply_markup=markup)
        global game_won
        if game_won:
            sm.clear()
            robot.send_message(call.message.chat.id, "All the rats are in a new bag! 😸")
            game_won = True
            game_started = False
        global game_lost
        if game_lost:
            sm.clear()
            robot.send_message(call.message.chat.id, "All the rats ran away! 😿")
            game_lost = True
            game_started = False


robot.polling(none_stop=True)
