"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    result = []
    previous = None
    for dummy_i in range(len(list1)):
        if list1[dummy_i] != previous:
            result.append(list1[dummy_i])
            previous = list1[dummy_i]
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    lst1 = remove_duplicates(list1)
    lst2 = remove_duplicates(list2)
    lst1_p = lst2_p = 0
    while lst1_p < len(lst1) and lst2_p < len(lst2):
        if lst1[lst1_p] == lst2[lst2_p]:
            result.append(lst1[lst1_p])
            lst1_p += 1
            lst2_p += 1
        elif lst1[lst1_p] < lst2[lst2_p]:
            lst1_p += 1
        else:
            lst2_p += 1
    return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    result = []
    lst1_p = lst2_p = 0
    while lst1_p < len(list1) and lst2_p < len(list2):
        if list1[lst1_p] == list2[lst2_p]:
            result.extend([list1[lst1_p]] * 2)
            lst1_p += 1
            lst2_p += 1
        elif list1[lst1_p] < list2[lst2_p]:
            result.append(list1[lst1_p])
            lst1_p += 1
        else:
            result.append(list2[lst2_p])
            lst2_p += 1
    result = result + list1[lst1_p:] if lst1_p < len(list1) else result + list2[lst2_p:]
    return result
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    else:
        mid = len(list1) / 2
        sorted_left = merge_sort(list1[:mid])
        sorted_right = merge_sort(list1[mid:])
        return merge(sorted_left, sorted_right)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    result = []
    if not word:
        result.append('')
        return result
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        for string in rest_strings:
            result += [string[:insert_pos] + first + string[insert_pos:] for insert_pos in range(len(string)+1)]
    return result + rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
