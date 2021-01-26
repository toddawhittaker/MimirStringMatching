# MimirStringMatching
A script for auto-grading string-based answers in MimirHQ

Mimir's support for auto-grading of fill-in-the-blank, matching, or other short
string-based answers is problematic. No rubrics are available for text-based answer
and many of these should be automated. This repository lets you have those kinds of
questions be auto-graded by using Levenshtein ratios (near matches)

## How to use
1. Create a new "Code Question" in Mimir.
1. Name your solution code file named "answer.txt"
1. Make a matching "answer.txt" in the student starter code with only the numbering
1. For grading, click "Add Test Case"
1. On the grading screen, name your test case and assign the *full* points
for the problem
1. Select a "Custom Test Case" for the test case type.
1. Turn on "Allow partial credit"
1. Turn off "Disable Internet Connections" 
1. Paste the following test script into the Bash script area:  
```bash
# To use this script:
#   Add "Optional" files containing your test cases
#   (file names must macth ".*Test.java$" regex) and
#   any other jar files or java files you want to compile
#   or include in the classpath. You could also wget
#   those file from a github source.

wget -q https://raw.githubusercontent.com/toddawhittaker/MimirStringMatching/master/mimir_string_matching.py
/usr/bin/python3.6 mimir_string_matching.py
```  
1. Create a file "expected.csv" and drag that into the "Files (optional)" section that
contains the set of expected answers (see below)

## Sample files
Here's what a sample `answer.txt` file would look like:
```text
// you can add comments that are ignored, e.g.
// Do not change numbering.
a. 
b. 
c. 
d. 
e. 
```

And here's what a sample `expected.csv` file would look like:
```csv
"a.","apple"
"b.","orange","mandarin"
"c.","pomegranate"
"d.","banana","plantain"
"e.","kiwi"
```

Notice that the `expected.csv` file has the same prefix as in the `answer.txt` file for
each line. That's how the student answers are correlated to the expected ones. Further,
you can create an arbitrarily long list of accepted answers for each prefix (these are
case insensitive). That's useful for things like true/false answers where you'd accept the
word or the letter.