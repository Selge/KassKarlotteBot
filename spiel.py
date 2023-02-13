import telebot
from telebot import types
import random


bot = telebot.TeleBot('6083048382:AAGNV4pgM3MIuaaxVq7kWo1nYEetEX4IfDQ')

item = {}
gameIsStart = False
gameGround = [" ", " ", " ",
              " ", " ", " ",
              " ", " ", " ", ]
playerSymbol = '🐱'
botSymbol = '🐀'
game_won = False
game_lost = False


def clear():
    global gameGround
    gameGround = [" ", " ", " ",
                  " ", " ", " ",
                  " ", " ", " ", ]


def win():
    if (gameGround[0] == playerSymbol and gameGround[1] == playerSymbol and gameGround[2] == playerSymbol or
        gameGround[3] == playerSymbol and gameGround[4] == playerSymbol and gameGround[5] == playerSymbol or
        gameGround[6] == playerSymbol and gameGround[7] == playerSymbol and gameGround[8] == playerSymbol or
        gameGround[1] == playerSymbol and gameGround[4] == playerSymbol and gameGround[7] == playerSymbol or
        gameGround[2] == playerSymbol and gameGround[5] == playerSymbol and gameGround[8] == playerSymbol or
        gameGround[3] == playerSymbol and gameGround[6] == playerSymbol and gameGround[9] == playerSymbol or
        gameGround[1] == playerSymbol and gameGround[5] == playerSymbol and gameGround[9] == playerSymbol or
        gameGround[3] == playerSymbol and gameGround[5] == playerSymbol and gameGround[7] == playerSymbol):
        global game_won
        game_won = True


def lose():
    if (gameGround[0] == botSymbol and gameGround[1] == botSymbol and gameGround[2] == botSymbol or
        gameGround[3] == botSymbol and gameGround[4] == botSymbol and gameGround[5] == botSymbol or
        gameGround[6] == botSymbol and gameGround[7] == botSymbol and gameGround[8] == botSymbol or
        gameGround[1] == botSymbol and gameGround[4] == botSymbol and gameGround[7] == botSymbol or
        gameGround[2] == botSymbol and gameGround[5] == botSymbol and gameGround[8] == botSymbol or
        gameGround[3] == botSymbol and gameGround[6] == botSymbol and gameGround[9] == botSymbol or
        gameGround[1] == botSymbol and gameGround[5] == botSymbol and gameGround[9] == botSymbol or
        gameGround[3] == botSymbol and gameGround[5] == botSymbol and gameGround[7] == botSymbol):
        global losebool
        game_lost = True


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Start game")
    markup.add(button)

    if message.text == "/start":
        bot.send_message(message.chat.id, """ 
            Seisid keldris koorepotid,
            koore kallal käisid rotid.

            Uhkat-tuhkat, kass Karlotte
            keldrisse läks püüdma rotte!

            Vöttis kaasa suured kotid,
            et saaks neisse panna rotid.

            Ah, see kaval kass Karlotte
            rüüdis suure hulga rotte!

            Kottidesse pani rotid
            ja siis selga vöttis kotid.

            Tuli keldrist kass Karlotte,
            kandis suuri rotikotte.

            Auke täis aga olid kotid,
            plehku panid köik ta rotid.

        This is a sad story about a cat named Karlotte, written by estonian poet Kalju Kangur.
        Karlotte once went for a rat hunt. She caught all the rats in the basement and put them to an old sack.
        But the sack was too old and all the rats ran away.
        Poor Karlotte!

        {0.first_name}! 
        Wanna help Karlotte 🐱 catch all the 🐀🐀🐀?
        """.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


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
        if gameGround[randomCell] == playerSymbol:
            randomCell = random.randint(0, 9)
        if gameGround[randomCell] == botSymbol:
            randomCell = random.randint(0, 9)
        if gameGround[randomCell] == " ":
            gameGround[randomCell] = botSymbol
        # player manager
        for i in range(9):
            if call.data == str(i):
                if (gameGround[i] == " "):
                    gameGround[i] = playerSymbol

            item[i] = types.InlineKeyboardButton(gameGround[i], callback_data=str(i))

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
