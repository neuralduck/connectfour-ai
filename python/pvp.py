import os

from connectfour import (
    Player,
    State,
    Status,
    Symbol,
    check,
    evaluate,
    move,
    print_board,
)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


game = State()
turn = 1
while True:
    status = check(game)
    if status != Status.IN_PROGRESS:
        print("\n")
        print_board(game)
        print("\n")
        match status:
            case Status.P1:
                print(f"{Symbol.P1} wins")
            case Status.P2:
                print(f"{Symbol.P2} wins")
            case Status.DRAW:
                print("Draw")
        break
    print("\n")
    print_board(game)
    print("\n")

    if turn:
        print(f"eval: {evaluate(game, Player.P1)}")
        p1 = int(input("Player 1: "))
        assert p1 in range(7)
        game = move(game, p1, Player.P1)
        turn = not (turn)
    else:
        print(f"eval: {evaluate(game, Player.P2)}")
        p2 = int(input("Player 2: "))
        assert p2 in range(7)
        game = move(game, p2, Player.P2)
        turn = not (turn)
