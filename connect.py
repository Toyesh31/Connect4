import numpy as np
import random
import time
import math

ROWS = 12
COLUMNS = 8
PLAYER = 0
AI = 1


def circ_slice(a, start, length):
    return (a * 2)[start:start+length]


def createBoard():
    board = np.zeros((ROWS, COLUMNS))
    return board


board = createBoard()


def dropPiece(board, row, col, piece):
    board[row][col] = piece


def isValid(board, col):
    try:
        return board[ROWS-1][col] == 0
    except:
        pass


def getRow(board, col):
    for i in range(ROWS):
        if board[i][col] == 0:
            return i


def horizontalCheck(board, piece):
    for i in range(ROWS):
        rlst = [i for i in list(board[i, :])]
        for j in range(COLUMNS):
            window = circ_slice(rlst, j, 4)
            if window.count(piece) == 4:
                return True
    return False


def verticalCheck(board, piece):
    for i in range(COLUMNS):
        clst = [int(i) for i in list(board[:, i])]
        for j in range(ROWS-3):
            window = clst[j:j+4]
            if window.count(piece) == 4:
                return True
    return False


def possitiveDiagonalCheck(board, piece):
    for i in range(ROWS-3):
        for j in range(COLUMNS-3):
            window = [board[i+k][j+k] for k in range(4)]
            if window.count(piece) == 4:
                return True
    return False


def negetiveDiagonalCheck(board, piece):
    for i in range(ROWS-3):
        for j in range(COLUMNS-3):
            window = [board[i+3-k][j+k] for k in range(4)]
            if window.count(piece) == 4:
                return True
    return False


def isWinning(board, piece):
    return horizontalCheck(board, piece) | verticalCheck(board, piece) | possitiveDiagonalCheck(board, piece) | negetiveDiagonalCheck(board, piece)


def evalScores(window, piece):
    score = 0
    opp_piece = 1
    if piece == 1:
        opp_piece = 2

    if window.count(piece) == 4:
        score += 42000
    elif (window.count(piece) == 3) & (window.count(0) == 1):
        score += 5
    elif (window.count(piece) == 2) & (window.count(0) == 2):
        score += 2
    if (window.count(opp_piece) == 3) & (window.count(0) == 1):
        score -= 4
    return score


def miniMaxScores(board, piece):
    score = 0

    # center colums
    clst1 = [int(i) for i in list(board[:, COLUMNS//2])]
    clst2 = [int(i) for i in list(board[:, (COLUMNS//2)-1])]
    c1count = clst1.count(piece)
    c2count = clst2.count(piece)
    score += c1count*1
    score += c2count*1

    # horizontal
    for i in range(ROWS):
        rlst = [int(i) for i in list(board[i, :])]
        for j in range(COLUMNS):
            window = circ_slice(rlst, j, 4)
            score += evalScores(window, piece)
    # vertical
    for i in range(COLUMNS):
        clst = [int(i) for i in list(board[:, i])]
        for j in range(ROWS-3):
            window = clst[j:j+4]
            score += evalScores(window, piece)

    # possitive diagonal
    for i in range(ROWS-3):
        for j in range(COLUMNS-3):
            window = [board[i+k][j+k] for k in range(4)]
            score += evalScores(window, piece)

    # negative diagonal
    for i in range(ROWS-3):
        for j in range(COLUMNS-3):
            window = [board[i+3-k][j+k] for k in range(4)]
            score += evalScores(window, piece)

    return score


def validColumns(board):
    return [i for i in range(COLUMNS) if isValid(board, i)]


# def selectColumn(board, piece):
#     valid_cols = validColumns(board)
#     best_score = 0
#     best_col = random.choice(valid_cols)
#     for col in valid_cols:
#         row = getRow(board, col)
#         tmp_board = board.copy()
#         dropPiece(tmp_board, row, col, piece)
#         score = miniMaxScores(tmp_board, piece)
#         # center columns
#         if (col == COLUMNS//2) | (col == (COLUMNS//2 - 1)):
#             score += 1
#         if score > best_score:
#             best_score = score
#             best_col = col
#     return best_col


def isTerminal(board):
    return isWinning(board, 1) | isWinning(board, 2) | (len(validColumns(board)) == 0)


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_cols = validColumns(board)
    terminal = isTerminal(board)
    if (depth == 0) | (terminal):
        if terminal:
            if isWinning(board, 2):
                return (None, 1000000000000)
            elif isWinning(board, 1):
                return (None, -1000000000000)
            else:
                return (None, 0)
        else:
            return (None, miniMaxScores(board, 2))
    if maximizingPlayer:
        value = -math.inf
        bestcol = random.choice(valid_cols)
        for col in valid_cols:
            row = getRow(board, col)
            tmpboard = board.copy()
            dropPiece(tmpboard, row, col, 2)
            nscore = minimax(tmpboard, depth-1, alpha, beta, False)[1]
            if nscore > value:
                value = nscore
                bestcol = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return bestcol, value
    else:
        value = math.inf
        bestcol = random.choice(valid_cols)
        for col in valid_cols:
            row = getRow(board, col)
            tmpboard = board.copy()
            dropPiece(tmpboard, row, col, 1)
            nscore = minimax(tmpboard, depth-1, alpha, beta, True)[1]
            if nscore < value:
                value = nscore
                bestcol = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return bestcol, value


game_over = False


turn = random.randint(PLAYER, AI)
player_name = input("Enter your name: ")
while not game_over:
    if turn == PLAYER:
        turnOver = False
        print(player_name)

        while not turnOver:
            col = int(input("Select colomn (0 - 7): "))
            if isValid(board, col):
                turnOver = True
                row = getRow(board, col)
                dropPiece(board, row, col, 1)
                print(np.flip(board, 0))
                if isWinning(board, 1):
                    print(player_name, "wins !!")
                    game_over = True
            else:
                print("Not valid")
    else:
        print('AI')
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        if isValid(board, col):
            row = getRow(board, col)
            dropPiece(board, row, col, 2)
            print(np.flip(board, 0))
            if isWinning(board, 2):
                print("AI wins !!")
                game_over = True

    turn ^= 1
