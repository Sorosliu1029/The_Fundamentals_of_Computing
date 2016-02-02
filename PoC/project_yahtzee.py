"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""


# Used to increase the timeout, if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    result = {}
    for dice in hand:
        result[dice] = result.get(dice, 0) + dice
    return max(result.values())


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    all_hands = gen_all_sequences(list(range(1, num_die_sides+1)), num_free_dice)
    all_results = [hand + held_dice for hand in all_hands]
    total_value = sum(list(map(score, all_results)))
    return float(total_value) / (num_die_sides ** num_free_dice)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    result = set([()])
    if len(hand) != 1:
        for item in gen_all_holds(hand[1:]):
            result.add((hand[0], ) + item)
            result.add(item)
        return result
    else:
        result.add((hand[0], ))
        return result

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    possible_holds = gen_all_holds(hand)
    result = (0.0, ())
    for hold in possible_holds:
        ex_val = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if ex_val > result[0]:
            result = (ex_val, hold)
    return result


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


run_example()


# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)
