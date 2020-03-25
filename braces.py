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


def count_test(brace_type: str, test_string: str):
    print(f"Testing {brace_type} brace count...")
    assert test_string.count(brace_type) == test_string.count(BRACES[brace_type])


def sequence_test(test_string: str):
    brace_count_by_type = {k: 0 for k in OPENER_LIST}
    print("Now testing char by char...\n")
    for idx, i in enumerate(test_string):
        print(test_string[:idx])
        if i in OPENER_LIST:
            brace_count_by_type[i] += 1
            currently_opened_brace = i
        elif i in CLOSER_LIST:
            assert currently_opened_brace == BRACES_REV[i], "Unexpected closing brace!"
            brace_count_by_type[BRACES_REV[i]] -= 1
            assert brace_count_by_type[BRACES_REV[i]] >= 0, "Too many closing braces!"


def find_first_brace(test_string: str):
    for i in test_string:
        if i in CLOSER_LIST:
            print("First brace in sequence is a closing one!")
            sys.exit(2)
        elif i in OPENER_LIST:
            return test_string.index(i)
    return -1


def find_last_brace(test_string: str):
    for idx, i in enumerate(test_string[::-1]):
        if i in OPENER_LIST:
            print("Last brace in sequence is an opening one!")
            sys.exit(2)
        if i in CLOSER_LIST:
            return len(test_string) - idx
    return -1


def find_first_brace_of_type(test_string: str, brace_type: str):
    for i in test_string:
        if i == brace_type:
            return test_string.index(i)
    return -1


def find_last_brace_of_type(test_string: str, brace_type: str):
    for idx, i in enumerate(test_string[::-1]):
        if i == BRACES[brace_type]:
            return len(test_string) - idx
    return -1


def cut_test_string(test_string: str):
    first_brace_index = find_first_brace(test_string)
    last_brace_index = find_last_brace(test_string)

    return test_string[first_brace_index:last_brace_index]


def parse_args():
    try:
        return sys.argv[1]
    except IndexError:
        print("Need to pass a brace string!")
        sys.exit(2)
    except Exception as ex:
        raise ex


def main():
    # reading passed string
    test_string = parse_args()

    # removing dangling symbols
    cut_string = cut_test_string(test_string)
    print(f"Test string is {cut_string}")

    # quick count test
    for brace_type in OPENER_LIST:
        count_test(brace_type, cut_string)

    # char-by-char test
    sequence_test(cut_string)


if __name__ == "__main__":
    main()
