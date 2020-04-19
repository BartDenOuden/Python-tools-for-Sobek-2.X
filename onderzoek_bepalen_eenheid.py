import math

import numpy as np


def e_power(x):
    return math.floor(math.log(abs(x), 10))


def multiple_for_locator(units_per_cm):
    power = e_power(units_per_cm)
    multiple = units_per_cm * 10 ** -power

    target_values = np.array([1, 2.5, 5, 10])
    borders = (target_values[1:] + target_values[:-1]) / 2

    for border, target_value in zip(borders, target_values):
        if multiple < border:
            multiple = target_value
            return multiple * 10**power
    return target_values[-1] * 10**power

print(multiple_for_locator(0.011))
