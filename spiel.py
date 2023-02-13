import types
import telebot
import random


bot = telebot.TeleBot('')

item = {}
gameIsStart = False
gameGround = [' ', ' ', ' ',
              ' ', ' ', ' ',
              ' ', ' ', ' ', ]
playerSymbol = '🐱'
botSymbol = '🐀'
game_won = False
game_lost = False


def clear():
    global gameGround
    gameGround = [' ', ' ', ' ',
                  ' ', ' ', ' ',
                  ' ', ' ', ' ', ]


def win(cell_1, cell_2, cell_3):
    if cell_1 == playerSymbol and cell_2 == playerSymbol and cell_3 == playerSymbol:
        print("win")
        global game_won
        game_won = True


def lose(cell_1, cell_2, cell_3):
    if cell_1 == botSymbol and cell_2 == botSymbol and cell_3 == botSymbol:
        print("lose")
        global losebool
        game_lost = True


def defend(cell_1, cell_2, posDef):
    if cell_1 == playerSymbol and cell_2 == playerSymbol:
        posDef = botSymbol


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
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
            # lose or win
            win(gameGround[1], gameGround[2], gameGround[3])
            win(gameGround[1], gameGround[5], gameGround[9])
            win(gameGround[6], gameGround[4], gameGround[2])
            win(gameGround[6], gameGround[7], gameGround[8])
            win(gameGround[0], gameGround[3], gameGround[6])
            lose(gameGround[0], gameGround[1], gameGround[2])
            lose(gameGround[0], gameGround[4], gameGround[8])
            lose(gameGround[6], gameGround[4], gameGround[2])
            lose(gameGround[6], gameGround[7], gameGround[8])
            lose(gameGround[0], gameGround[3], gameGround[6])

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
