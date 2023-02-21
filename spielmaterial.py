game_cell = {}
gameboard = 9 * [" "]
player_sign = '🐱'
robot_sign = '🐀'


def winner(cell_1, cell_2, cell_3):
    if cell_1 == player_sign and cell_2 == player_sign and cell_3 == player_sign:
        global game_won
        game_won = True


def loser(cell_1, cell_2, cell_3):
    if cell_1 == robot_sign and cell_2 == robot_sign and cell_3 == robot_sign:
        global losebool
        game_lost = True


def defend(cell_1, cell_2, posDef):
    if cell_1 == player_sign and cell_2 == player_sign:
        posDef = robot_sign


def clear():
    global gameboard
    gameboard = 9 * [" "]


def message():
    karlotte = """ 
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
        """
    return karlotte
