import telebot
from telebot import types
import random

import key
import spielmaterial as sm


bot = telebot.TeleBot(key.get_key())

cell = {}
gameIsStart = False
game_won = False
game_lost = False


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
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
            bot.send_message(message.chat.id, "use /help for assist!")

    if gameIsStart == True:
        item = {}
        bot.send_message(message.chat.id, "The hunt is started")
        global markup
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(0, 9):
            item[i] = types.InlineKeyboardButton(gameGround[i], callback_data=str(i))
        markup.row(item[0], item[1], item[2])
        markup.row(item[3], item[4], item[5])
        markup.row(item[6], item[7], item[8])
        bot.send_message(message.chat.id, "Choose a cell", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callbackInline(call):
    if (call.message):
        randomCell = random.randint(0, 9)
        if gameGround[randomCell] == sm.player_sign:
            randomCell = random.randint(0, 9)
        if gameGround[randomCell] == sm.robot_sign:
            randomCell = random.randint(0, 9)
        if gameGround[randomCell] == " ":
            gameGround[randomCell] = sm.robot_sign

        for i in range(9):
            if call.data == str(i):
                if (gameGround[i] == " "):
                    gameGround[i] = playerSymbol

            sm.win(gameGround[0], gameGround[1], gameGround[2])
            sm.win(gameGround[0], gameGround[4], gameGround[8])
            sm.win(gameGround[2], gameGround[4], gameGround[6])
            sm.win(gameGround[3], gameGround[4], gameGround[5])
            sm.win(gameGround[6], gameGround[7], gameGround[8])
            sm.win(gameGround[0], gameGround[3], gameGround[6])
            sm.win(gameGround[1], gameGround[4], gameGround[7])
            sm.win(gameGround[2], gameGround[5], gameGround[8])
            sm.lose(gameGround[0], gameGround[1], gameGround[2])
            sm.lose(gameGround[0], gameGround[4], gameGround[8])
            sm.lose(gameGround[2], gameGround[4], gameGround[6])
            sm.lose(gameGround[3], gameGround[4], gameGround[5])
            sm.lose(gameGround[6], gameGround[7], gameGround[8])
            sm.lose(gameGround[0], gameGround[3], gameGround[6])
            sm.lose(gameGround[1], gameGround[4], gameGround[7])
            sm.lose(gameGround[2], gameGround[5], gameGround[8])

            cell[i] = types.InlineKeyboardButton(gameGround[i], callback_data=str(i))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Catch all the rats!',
                              reply_markup=None)
        global markup
        markup.row(cell[0], cell[1], cell[2])
        markup.row(cell[3], cell[4], cell[5])
        markup.row(cell[6], cell[7], cell[8])

        bot.send_message(call.message.chat.id, "Choose a cell", reply_markup=markup)
        global game_won
        if game_won:
            clear()
            bot.send_message(call.message.chat.id, "All the rats are in a new bag! 😸")
            game_won = True
            gameIsStart = False
        global game_lost
        if game_lost:
            clear()
            bot.send_message(call.message.chat.id, "All the rats ran away! 😿")
            game_lost = True
            gameIsStart = False


bot.polling(none_stop=True)




# item = {}
# gameIsStart = False
# game_won = False
# game_lost = False
#
#
# @bot.message_handler(commands=['start'])
# def welcome(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button = types.KeyboardButton("Start game")
#     markup.add(button)
#

#
#
# @bot.message_handler(content_types=['text'])
# def mess(message):
#     if message.chat.type == 'private':
#         if message.text == "Start game":
#             global gameIsStart
#             gameIsStart = True
#         else:
#             bot.send_message(message.chat.id, "use /start to play!")
#
#     if gameIsStart == True:
#         item = {}
#         bot.send_message(message.chat.id, "The hunt is started")
#         global markup
#         markup = types.InlineKeyboardMarkup(row_width=3)
#         for i in range(0, 9):
#             item[i] = types.InlineKeyboardButton(sm.board[i], callback_data=str(i))
#         markup.row(item[0], item[1], item[2])
#         markup.row(item[3], item[4], item[5])
#         markup.row(item[6], item[7], item[8])
#         bot.send_message(message.chat.id, "Choose a cell", reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callbackInline(call):
#     if (call.message):
#         while True:
#             the_board = [' '] * 10
#             game_is_active = True
#             turn = 'Human'
#
#             while game_is_active:
#                 if turn == 'Human':
#                     move = sm.get_player_move(the_board)
#                     sm.make_move(the_board, sm.player_sign, move)
#
#                     if sm.is_winner(the_board, sm.player_sign):
#                         sm.draw_board(the_board)
#                         print('Congrats! You have won the game!')
#                         game_is_active = False
#                     else:
#                         if sm.is_board_full(the_board):
#                             sm.draw_board(the_board)
#                             print('The game is a tie!')
#                             break
#                         else:
#                             turn = 'Computer'
#
#                 else:
#                     move = sm.get_computer_move(the_board, sm.computer_sign)
#                     sm.make_move(the_board, sm.computer_sign, move)
#                     the_board[move] = sm.computer_sign
#
#                     if sm.is_winner(the_board, sm.player_sign):
#                         sm.draw_board(the_board)
#                         print('The computer has beaten you! You lose.')
#                         game_is_active = False
#                     else:
#                         if sm.is_board_full(the_board):
#                             sm.draw_board(the_board)
#                             print('The game is a tie!')
#                             break
#                         else:
#                             turn = 'Human'
#         #
#         # randomCell = sm.get_computer_move(sm.board, sm.computer_sign)
#         # if sm.board[randomCell] == sm.player_sign:
#         #     randomCell = random.randint(0, 9)
#         # if sm.board[randomCell] == sm.computer_sign:
#         #     randomCell = random.randint(0, 9)
#         # if sm.board[randomCell] == " ":
#         #     sm.board[randomCell] = sm.computer_sign
#
#         # update cells
#         bot.edit_message_text(chat_id=call.message.chat.id,
#                               message_id=call.message.message_id,
#                               text='Catch all rats!',
#                               reply_markup=None)
#         global markup
#         markup.row(item[0], item[1], item[2])
#         markup.row(item[3], item[4], item[5])
#         markup.row(item[6], item[7], item[8])
#
#         bot.send_message(call.message.chat.id, "Choose a cell", reply_markup=markup)
#         global game_won
#         if game_won:
#             bot.send_message(call.message.chat.id, "All the rats are in a new bag! 😸")
#             game_won = True
#             gameIsStart = False
#         global game_lost
#         if game_lost:
#             bot.send_message(call.message.chat.id, "All the rats ran away! 😿")
#             game_lost = True
#             gameIsStart = False
#
#
# bot.polling(none_stop=True)
