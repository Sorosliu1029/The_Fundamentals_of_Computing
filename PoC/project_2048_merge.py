"""
Merge function for 2048 game.
"""


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    start_idx = 0
    end_idx = 1
    dummy_line = [value for value in line if value]
    if len(dummy_line) < 2:
        return dummy_line + [0] * (len(line)-len(dummy_line))
    result = []
    while end_idx < len(dummy_line):
        if dummy_line[start_idx] == dummy_line[end_idx]:
            result.append(dummy_line[start_idx] * 2)
            start_idx = end_idx + 1
            end_idx += 1
        else:
            result.append(dummy_line[start_idx])
            start_idx = end_idx
        if end_idx == len(dummy_line)-1:
            result.append(dummy_line[end_idx])
        end_idx += 1
    return result + [0] * (len(line) - len(result))

# test_list = [
# [2, 0, 2, 4],
# [0, 0, 2, 2],
# [2, 2, 0, 0],
# [2, 2, 2, 2, 2],
# [8, 16, 16, 8]
# ]
# for test in test_list:
#     print merge(test)
