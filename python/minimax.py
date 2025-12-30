import os

from connectfour import (
    Player,
    State,
    Status,
    Symbol,
    available_moves,
    check,
    evaluate,
    move,
    print_board,
)


def minimax(
    state: State, player: Player, alpha=-float("inf"), beta=float("inf"), depth=1
):
    global calls
    calls += 1
    match player:
        case Player.P1:
            best_score = [None, -float("inf")]
        case Player.P2:
            best_score = [None, float("inf")]
    status = check(state)
    if (status != Status.IN_PROGRESS) or (depth == 8):
        return [None, evaluate(state, player)]
    preferred = [3, 4, 2, 5, 1, 6, 0]

    for choice in preferred:
        if choice in available_moves(state):
            next_state = move(state, choice, player)
            if player == Player.P1:
                _, score = minimax(next_state, Player.P2, alpha, beta, depth + 1)  # type: ignore
            else:
                _, score = minimax(next_state, Player.P1, alpha, beta, depth + 1)  # type: ignore
            if (player == Player.P1) and (score > best_score[1]):
                best_score = [choice, score]
                alpha = max(alpha, best_score[1])
                if alpha >= beta:
                    break
            if (player == Player.P2) and (score < best_score[1]):
                best_score = [choice, score]
                beta = min(beta, best_score[1])
                if beta <= alpha:
                    break
    return best_score


if __name__ == "__main__":
    calls = 0

    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    first = input("want to go first? [Y/n]").lower()
    game = State()
    if first in ("", "y"):
        turn = 1
    else:
        turn = 0
    while True:
        status = check(game)
        print(status)
        if status != Status.IN_PROGRESS:
            print(status)
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
        print("\n")
        if turn:
            p1 = int(input("You: "))
            assert p1 in range(9)
            game = move(game, p1, Player.P1)
            turn = not (turn)
        else:
            p2 = minimax(game, Player.P2)
            print(p2)
            p2 = p2[0]
            assert p2 in range(9)
            game = move(game, p2, Player.P2)
            turn = not (turn)

    print(f"recursive calls = {calls}")
