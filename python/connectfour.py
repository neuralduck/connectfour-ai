from dataclasses import dataclass
from enum import Enum, auto

ROW = 6
COL = 7

horizontal = 15
vertical = 2113665
diag1 = 16843009
diag2 = 2130440

WINDOWS = []
for i in range(ROW):
    for j in range(4):
        WINDOWS.append(horizontal << i * 7 + j)
for i in range(21):
    WINDOWS.append(vertical << i)
for i in range(3):
    for j in range(4):
        WINDOWS.append(diag1 << i * 7 + j)
for i in range(3):
    for j in range(4):
        WINDOWS.append(diag2 << i * 7 + j)


class Status(Enum):
    P1 = auto()
    P2 = auto()
    DRAW = auto()
    IN_PROGRESS = auto()


class Player(Enum):
    P1 = auto()
    P2 = auto()


@dataclass
class State:
    P1: int = 0
    P2: int = 0


@dataclass
class Symbol:
    P1 = "\N{BLACK CIRCLE}"
    P2 = "\N{WHITE CIRCLE}"


def move(state: State, choice: int, player: Player) -> State:
    assert choice in range(COL)
    for i in range(choice, ROW * COL, COL):
        choice_mask = 1 << i
        if (not state.P1 & choice_mask) and (not state.P2 & choice_mask):
            match player:
                case Player.P1:
                    return State(P1=state.P1 | choice_mask, P2=state.P2)
                case Player.P2:
                    return State(P1=state.P1, P2=state.P2 | choice_mask)
    return state


def available_moves(state: State):
    moves = []
    for c in range(COL):
        top = 1 << (c + (ROW - 1) * COL)
        if not (state.P1 & top or state.P2 & top):
            moves.append(c)
    return moves


def evaluate(state: State, player: Player):
    result = check(state)
    if result != Status.IN_PROGRESS:
        match result:
            case Status.P1:
                return 100000
            case Status.P2:
                return -100000
            case Status.DRAW:
                return 0
    value = 0
    for window in WINDOWS:
        p1 = (state.P1 & window).bit_count()
        p2 = (state.P2 & window).bit_count()
        if p1 and p2:  # one p1/p2 and two p2/p1 in a window of 4
            continue
        if player == Player.P1:
            if p1 == 3:
                value += 200
            if p1 == 2:
                value += 100
            if p2 == 3:
                value -= 100
            if p2 == 2:
                value -= 50
        else:
            if p1 == 3:
                value += 100
            if p1 == 2:
                value += 50
            if p2 == 3:
                value -= 200
            if p2 == 2:
                value -= 100
    return value


def check(state: State):
    if (
        state.P1 & (state.P1 >> 1) & (state.P1 >> 2) & (state.P1 >> 3)
        or (state.P1 & (state.P1 >> 7) & (state.P1 >> 14) & (state.P1 >> 21))
        or (state.P1 & (state.P1 >> 6) & (state.P1 >> 12) & (state.P1 >> 18))
        or (state.P1 & (state.P1 >> 8) & (state.P1 >> 16) & (state.P1 >> 24))
    ):
        return Status.P1
    elif (
        state.P2 & (state.P2 >> 1) & (state.P2 >> 2) & (state.P2 >> 3)
        or (state.P2 & (state.P2 >> 7) & (state.P2 >> 14) & (state.P2 >> 21))
        or (state.P2 & (state.P2 >> 6) & (state.P2 >> 12) & (state.P2 >> 18))
        or (state.P2 & (state.P2 >> 8) & (state.P2 >> 16) & (state.P2 >> 24))
    ):
        return Status.P2
    elif state.P1 | state.P2 == 4398046511103:
        return Status.DRAW
    else:
        return Status.IN_PROGRESS


def print_board(state: State):
    board = [" "] * ROW * COL
    for i in range(ROW * COL):
        if state.P1 & (1 << i):
            board[i] = Symbol.P1
        elif state.P2 & (1 << i):
            board[i] = Symbol.P2
    board = board[::-1]
    ref = [str(i) for i in range(COL)]
    print("| " + " | ".join(ref[::-1]))
    print("-" * (len(ref) * 4))
    for i in range(ROW):
        print("| " + " | ".join(board[i * COL : (i + 1) * COL]))


"""
41 40 39 38 37 36 35
34 33 32 31 30 29 28
27 26 25 24 23 22 21
20 19 18 17 16 15 14
13 12 11 10  9  8  7
 6  5  4  3  2  1  0


6  5  4  3  2  1  0
.  X  X  X  X  .  .


m        → bits at 5,4,3,2
m >> 1   → bits at 4,3,2,1
m >> 2   → bits at 3,2,1,0
m >> 3   → bits at 2,1,0,-1

m = bits
if m & (m >> 1) & (m >> 2) & (m >> 3): win        # horizontal
if m & (m >> 7) & (m >> 14) & (m >> 21): win     # vertical
if m & (m >> 6) & (m >> 12) & (m >> 18): win     # diag /
if m & (m >> 8) & (m >> 16) & (m >> 24): win     # diag \

"""


if __name__ == "__main__":
    gamestate = State()
    print(available_moves(gamestate))
    gamestate = move(gamestate, 0, Player.P1)
    print(gamestate)
    print("\n")

    print(available_moves(gamestate))
    gamestate = move(gamestate, 1, Player.P1)
    print(gamestate)
    print("\n")

    print(available_moves(gamestate))
    gamestate = move(gamestate, 2, Player.P1)
    print(gamestate)
    print("\n")

    print(available_moves(gamestate))
    gamestate = move(gamestate, 3, Player.P1)
    print(gamestate)
    print("\n")

    print(available_moves(gamestate))
    gamestate = move(gamestate, 2, Player.P2)
    print(gamestate)
    print("\n")

    print("\n")
    print_board(gamestate)
    print(check(gamestate))
    print(evaluate(gamestate))
