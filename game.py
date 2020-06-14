import board as board


def get_player_move(b, jump=False, move_from=()):
    if b.turn == b.WHITE:
        print("WHITE'S TURN")
    else:
        print("BLACK'S TURN")
    if move_from != ():
        prompt = "Select destination for next jump from" + str(chr(move_from[0] + 97)) + str(move_from[1] + 1) + "\n>>"
        while True:
            move = input(prompt).lower()
            if len(move) not in [2]:
                print("That is not a valid statement, try again. ")
                continue
            move_to = (ord(move[3]) - 97, int(move[4]) - 1)
            if not b.is_valid_selection(*move_from):
                continue
            if not b.is_valid_move(*move_from, *move_to):
                continue
            break
    else:
        prompt = "Select one of your pieces and destination eg. f1 e2\n>>"
        while True:  # loop until proper input is given
            move = input(prompt).lower()
            if len(move) not in [5]:
                print("That is not a valid statement, try again. ")
                continue
            move_from = (ord(move[0]) - 97, int(move[1]) - 1)
            move_to = (ord(move[3]) - 97, int(move[4]) - 1)
            if not b.is_valid_selection(*move_from):
                continue
            if not b.is_valid_move(*move_from, *move_to):
                continue
            break
    if b.player_move(*move_from, *move_to):
        b.jump = False
        if len(b.get_jumps(*move_to)) > 0:
            get_player_move(b, move_to)
        else:
            b.switch_turn()


def game():
    n = -1
    while n not in [1, 2]:
        n = input("Choose mode:\n1 = player vs computer\n2 = player vs player\n>>")
        try:
            n = int(n)
        except ValueError:
            print("Please input 1 or 2")

    if n == 2:
        b = board.Board()
        print(b)
        while not b.game_won:
            get_player_move(b)
        if b.game_won == b.WHITE['player']:
            print("White wins. Congrats!")
        elif b.game_won == b.BLACK['player']:
            print("Black wins. Congrats!")
    else:
        pass


if __name__ == '__main__':
    print("Hello")
    game()
    print("Game over")