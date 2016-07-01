def probability(outcomes):
    result = 1.0
    for num in outcomes:
        if num == 1:
            result *= 0.1
        elif num == 2:
            result *= 0.2
        elif num == 3:
            result *= 0.3
        elif num == 4:
            result *= 0.15
        elif num == 5:
            result *= 0.05
        elif num == 6:
            result *= 0.2
    return result

print probability([1])
print probability([4, 2, 6, 4, 2, 4, 5, 5, 5, 5, 1, 2, 2, 6, 6, 4, 6, 2, 3, 5,
                    5, 2, 1, 5, 5, 3, 2, 1, 4, 4, 1, 6, 6, 4, 6, 2, 4, 3, 2, 5,
                    1, 3, 5, 4, 1, 2, 3, 6, 1])
