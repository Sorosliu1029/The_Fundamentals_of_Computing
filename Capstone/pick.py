def pick_a_number(board):
    result = [0, 0]
    length = len(board)
    for i in range(length):
        if board[0] > board[-1]:
            result[i%2] += board.pop(0)
        else:
            result[i%2] += board.pop()
    return result

print pick_a_number([12, 9, 7, 3, 4, 7, 4, 7, 3, 16, 4, 8, 12, 1, 2, 7, 11, 6,
                    3, 9, 7, 1])
