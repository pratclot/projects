"""
Run tests with:
python3 -m doctest braces.py

Run the program with:
python3 braces.py '[)(][][][(])'
"""

import sys
from collections import namedtuple

BracePair = namedtuple("brace_pair", "opener closer")
BRACES = [
    BracePair("(", ")"),
    BracePair("[", "]"),
    BracePair("{", "}")
]
OPENER_LIST = [x.opener for x in BRACES]
CLOSER_LIST = [x.closer for x in BRACES]
BRACES = {k: v for k, v in zip(OPENER_LIST, CLOSER_LIST)}
BRACES_REV = {v: k for k, v in BRACES.items()}


def count_test(test_string: str):
    """

    :param test_string:
    :return:

    >>> count_test('[[[]]]')
    Testing ( brace count...
    Testing [ brace count...
    Testing { brace count...
    """
    for brace_type in OPENER_LIST:
        count_test_by_brace(brace_type, test_string)


def count_test_by_brace(brace_type: str, test_string: str):
    """

    :param brace_type:
    :param test_string:
    :return:

    >>> count_test_by_brace('[', '[[[]]]')
    Testing [ brace count...
    """
    print(f"Testing {brace_type} brace count...")
    assert test_string.count(brace_type) == test_string.count(BRACES[brace_type]),\
        f"Brace {brace_type} count is wrong!"


def sequence_test(test_string: str):
    """

    :param test_string:
    :return:

    >>> sequence_test('[[[]]]')
    Testing char by char...
    [
    [[
    [[[
    [[[]
    [[[]]
    [[[]]]
    The string is fine!
    """
    brace_count_by_type = {k: 0 for k in OPENER_LIST}
    print("Testing char by char...")
    currently_opened_brace, previously_opened_brace = [None] * 2
    for idx, i in enumerate(test_string):
        print(f"{test_string[:idx+1]}")
        if i in OPENER_LIST:
            brace_count_by_type[i] += 1
            if isinstance(currently_opened_brace, str):
                previously_opened_brace, currently_opened_brace = currently_opened_brace, i
            else:
                currently_opened_brace = i
        elif i in CLOSER_LIST:
            if currently_opened_brace != BRACES_REV[i]:
                print("Unexpected closing brace!")
                sys.exit(2)
            elif brace_count_by_type[BRACES_REV[i]] < 1:
                print("Too many closing braces!")
                sys.exit(2)
            brace_count_by_type[BRACES_REV[i]] -= 1
            currently_opened_brace = previously_opened_brace
    print("The string is fine!")


def find_first_brace(test_string: str):
    """

    :param test_string:
    :return:

    >>> find_first_brace('[[[]]]')
    0
    """
    for i in test_string:
        if i in CLOSER_LIST:
            print("First brace in sequence is a closing one!")
            sys.exit(2)
        elif i in OPENER_LIST:
            return test_string.index(i)
    return -1


def find_last_brace(test_string: str):
    """

    :param test_string:
    :return:

    >>> find_last_brace('[[[]]]')
    6
    """
    for idx, i in enumerate(test_string[::-1]):
        if i in OPENER_LIST:
            print("Last brace in sequence is an opening one!")
            sys.exit(2)
        if i in CLOSER_LIST:
            return len(test_string) - idx
    return -1


def find_first_brace_of_type(test_string: str, brace_type: str):
    """

    :param test_string:
    :param brace_type:
    :return:

    >>> find_first_brace_of_type('[[[]]]', '[')
    0
    """
    for i in test_string:
        if i == brace_type:
            return test_string.index(i)
    return -1


def find_last_brace_of_type(test_string: str, brace_type: str):
    """

    :param test_string:
    :param brace_type:
    :return:


    >>> find_last_brace_of_type('[[[]]]', '[')
    6
    """
    for idx, i in enumerate(test_string[::-1]):
        if i == BRACES[brace_type]:
            return len(test_string) - idx
    return -1


def cut_test_string(test_string: str):
    """

    :param test_string:
    :return:

    >>> cut_test_string('[[[]]]')
    '[[[]]]'
    """
    first_brace_index = find_first_brace(test_string)
    last_brace_index = find_last_brace(test_string)

    return test_string[first_brace_index:last_brace_index]


def parse_args():
    """

    :return:

    >>> parse_args()
    'braces.py'
    """
    try:
        return sys.argv[1]
    except IndexError:
        print("Need to pass a brace string!")
        sys.exit(2)
    except Exception as ex:
        raise ex


def main():
    """

    :return:
    """
    # reading passed string
    test_string = parse_args()

    # removing dangling symbols, executes small sanity check for first and last braces
    cut_string = cut_test_string(test_string)
    print(f"Test string is {cut_string}")

    # quick count test
    count_test(cut_string)

    # char-by-char test
    sequence_test(cut_string)


if __name__ == "__main__":
    main()
