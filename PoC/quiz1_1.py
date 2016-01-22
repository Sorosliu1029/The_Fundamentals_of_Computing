def appendsums(lst):
    """
    Repeatedly append the sum of the current last three elements of lst to lst.
    """
    for idx in range(25):
        lst.append(sum(lst[-3:]))

sum_three = [0, 1, 2]
appendsums(sum_three)
print sum_three[20]
