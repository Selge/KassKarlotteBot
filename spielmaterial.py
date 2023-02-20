import random


board = 10 * [" "]
player_sign = '🐱'
computer_sign = '🐀'

def make_move(board, sign, move):
    board[move] = sign


def is_winner(board, sign):
    return ((board[1] == sign and board[2] == sign and board[3] == sign) or
            (board[4] == sign and board[5] == sign and board[6] == sign) or
            (board[7] == sign and board[8] == sign and board[9] == sign) or
            (board[1] == sign and board[4] == sign and board[7] == sign) or
            (board[2] == sign and board[5] == sign and board[8] == sign) or
            (board[3] == sign and board[6] == sign and board[9] == sign) or
            (board[1] == sign and board[5] == sign and board[9] == sign) or
            (board[3] == sign and board[5] == sign and board[7] == sign))


def get_board_copy(board):
    board_copy = []
    for i in board:
        board_copy.append(i)
    return board_copy


def is_space_free(board, move):
    return board[move] == ' '


def choose_random_move_from_list(board, moves_list):
    possible_moves = []
    for i in moves_list:
        if is_space_free(board, i):
            possible_moves.append(i)

    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    else:
        return None


def get_computer_move(board, computer_sign):
    even_moves = [2, 4, 6, 8]
    odd_moves = [1, 3, 7, 9]

    for i in range(1, 10):
        board_copy = get_board_copy(board)
        if is_space_free(board_copy, i):
            make_move(board_copy, computer_sign, i)
            if is_winner(board_copy, computer_sign):
                return i

    for i in range(1, 10):
        board_copy = get_board_copy(board)
        if is_space_free(board_copy, i):
            make_move(board_copy, player_sign, i)
            if is_winner(board_copy, player_sign):
                return i

    move = choose_random_move_from_list(board, odd_moves)
    if move != None:
        return move

    if is_space_free(board, 5):
        return 5

    return choose_random_move_from_list(board, even_moves)


def is_board_full(board):
    for i in range(1, 10):
        if is_space_free(board, i):
            return False
    return True


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
