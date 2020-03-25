"""
Run tests with:
python3 -m doctest braces.py

Run the program with:
python3 braces.py '[)(][][][(])'
"""

import sys
from collections import namedtuple, deque

BracePair = namedtuple("brace_pair", "opener closer")
BRACES = [
    BracePair("(", ")"),
    BracePair("[", "]"),
    BracePair("{", "}")
]
OPENER_LIST = [x.opener for x in BRACES]
CLOSER_LIST = [x.closer for x in BRACES]
BRACES = {k: v for k, v in zip(OPENER_LIST, CLOSER_LIST)}


def smart_sequence_test(test_string: str):
    """
    >>> smart_sequence_test('[()][][][]()')
    True
    """
    parsed_braces = deque()
    for i in test_string:
        if i in OPENER_LIST + CLOSER_LIST:
            if i in CLOSER_LIST:
                try:
                    if i != BRACES[parsed_braces.pop()]:
                        fail()
                except IndexError:
                    fail()
                continue
            parsed_braces.append(i)
    if len(parsed_braces) != 0:
        fail()
    print("True")


def fail():
    print("False")
    sys.exit(2)


def parse_args():
    """
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
    test_string = parse_args()
    smart_sequence_test(test_string)


if __name__ == "__main__":
    main()
