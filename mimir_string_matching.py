#!/usr/bin/python3.6

import os
import csv
import re
import sys
import getopt
import numpy as np

USAGE = f"Usage: python {sys.argv[0]} [--help] | [-a <student_answers_file>] [-e <expected_answers_csv>] [-p <all|none|marks|solutions>]"

# what levenshtein ratio is close enough for word matches?
MIN_RATIO = 0.85

# code for levenshtein_ratio taken from
# https://www.datacamp.com/community/tutorials/fuzzy-string-python


def levenshtein_ratio(s, t, ratio_calc=True):
    """ levenshtein_ratio:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    rows = len(s) + 1
    cols = len(t) + 1
    distance = np.zeros((rows, cols), dtype=int)

    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                if ratio_calc:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row - 1][col] + 1,
                                     distance[row][col - 1] + 1,
                                     distance[row - 1][col - 1] + cost)
    if ratio_calc:
        Ratio = ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))
        return Ratio
    else:
        return "The strings are {} edits away".format(distance[row][col])


def remove_comments(s):
    i = s.find("//")
    if i >= 0:
        return s[0:i].strip()
    return s.strip()


def no_blanks(s):
    return "" != s


def matches(expected, actual):
    ratio = levenshtein_ratio(expected.lower(), actual.lower())
    return ratio > MIN_RATIO


def extract_answers(number, expecteds, all_answers):
    s = fr'{number}\s*(.+)'
    p = re.compile(s)
    for answer in all_answers:
        m = p.match(answer)
        if m:
            actual = m.group(1)
            for expected in expecteds:
                result = matches(expected, actual)
                if result:
                    return (result, expected, actual)
            return (False, expecteds[0], actual)
    return (False, expecteds[0], None)


def parse(args):
    # default file names
    student_answers = 'answer.txt'
    expected_answers = 'expected.csv'
    output_opt = 'all'
    options, remainder = getopt.getopt(args, 'ha:e:p:', ['help', 'answers=', 'expected=', 'print='])
    for opt, arg in options:
        if opt in ('-h', '--help'):
            print(USAGE)
            sys.exit()
        elif opt in ('-a', '--answers'):
            student_answers = arg
        elif opt in ('-e', '--expected'):
            expected_answers = arg
        elif opt in ('-p', '--print'):
            output_opt = arg
        else:
            print(USAGE)
            sys.exit()
    return (student_answers, expected_answers, output_opt)


def main(args):
    student_answers, expected_answers, output_opt = parse(args)
    
    if not os.path.exists(expected_answers):
        raise Exception(f"Could not find file '{expected_answers}'")
    else:
        with open(expected_answers) as f:
            reader = csv.reader(f)
            expected = {
                rows[0]: list(filter(no_blanks, map(str.strip, rows[1:])))
                for rows in reader
            }

    if not os.path.exists(student_answers):
        raise Exception(f"Could not find file '{student_answers}'")
    else:
        with open(student_answers) as f:
            answers = list(filter(no_blanks, map(remove_comments, f.readlines())))

    results = {k: extract_answers(k, v, answers) for k, v in expected.items()}

    count_right = 0
    count_total = 0
    percent = 0
    with open('DEBUG', 'w') as f:
        for k, v in results.items():
            if v[0]:
                count_right = count_right + 1
            count_total = count_total + 1
            if output_opt in ('all', 'marks', 'solutions'):
                print(f"{k} {'Correct.' if v[0] else 'Incorrect.'} ", file=f, end='')
            if output_opt in ('all', 'solutions'):
                print(f"Expected '{v[1]}'. ", file=f, end='')
            if output_opt in ('all', 'solutions', 'marks'):
                print(f"Was '{v[2]}'.", file=f, end='')
            if output_opt in ('all', 'solutions', 'marks'):
                print('', file=f)
        percent = count_right * 100 // count_total
        if output_opt in ('all', 'marks', 'solutions'):
            print(f"{count_right} out of {count_total} correct. Your score is {percent}%.", file=f)

    with open('OUTPUT', 'w') as f:
        print(percent, file=f)

if __name__ == "__main__":
    main(sys.argv[1:])

