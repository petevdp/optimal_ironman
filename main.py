from typing import NamedTuple
import math
import numpy as np
import json
import matplotlib

matplotlib.use('WebAgg')

import matplotlib.pyplot as plt


class CharRating(NamedTuple):
    rating: float
    name: str


def main():
    with open('ratings.json') as f:
        ratings = json.load(f)
    with open('tier_list.json') as f:
        tier_list = json.load(f)

    with open('characters_in_order.json') as f:
        chars_in_order = json.load(f)

    char_ratings = [CharRating(*pair) for pair in zip(ratings, tier_list)]

    def plot_best_fit():
        x = np.array([*range(26)])
        a, b = np.polyfit(x, ratings, 1)
        plt.scatter(x, ratings)
        plt.plot(x, a * x + b)
        plt.show()

    min_distance = math.inf
    min_ordering = None

    max_distance = 0
    max_ordering = None

    for offset in range(26):
        ordering = []
        for relative_idx in range(26):
            abs_idx = (offset + relative_idx) % 26
            ordering.append(chars_in_order[abs_idx])
        distance = reorder_distance(ordering, [*reversed(tier_list)])
        if distance < min_distance:
            min_distance = distance
            min_ordering = ordering
        if distance > max_distance:
            max_distance = distance
            max_ordering = ordering


    print(min_distance,min_ordering)

def reorder_distance(l_a, l_b):
    acc_distance = 0
    for idx_a, a in enumerate(l_a):
        idx_b = l_b.index(a)
        distance = abs(idx_a - idx_b)
        acc_distance += distance
    return acc_distance / len(l_a)


if __name__ == "__main__":
    main()
