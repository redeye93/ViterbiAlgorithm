import sys
import os
from collections import Counter


def count_c(x, y):
    if len(x)<len(y):
        (x, y) = (y, x)

    a = Counter(x)
    b = Counter(y)

    return sum(min(b[key], value) for (key, value) in a.items())


if len(sys.argv) == 3:
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    if not os.path.exists(file1) or not os.path.exists(file2):
        print('One of the files is missing')
        exit(1)

    correct = 0
    incorrect = 0

    with open(file1, encoding='utf8') as text1:
        with open(file2, encoding='utf8') as text2:
            for (x, y) in zip(text1, text2):
                x = x.strip()
                y = y.strip()
                x = x.split()
                y = y.split()
                matching = count_c(x, y)

                correct += matching
                incorrect += len(x) - matching

    print(correct)
    print(incorrect)
    print(correct + incorrect)
    print(1.0 * correct / (correct + incorrect))

    text1.close()
    text2.close()
else:
    print('Insufficient number of arguments')
    exit(1)