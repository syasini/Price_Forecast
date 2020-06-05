"""This module contains functions for cleaning the input data"""

import numpy as np


def clean_vol(value):
    """clean values in the Vol. column"""

    if value == "-":
        return np.nan
    elif value.endswith("K"):
        return np.float32(value[:-1])
    else:
        return np.float32(value)


def clean_change(value):
    """clean values in the Change column"""

    if value.endswith("%"):
        return np.float32(value[:-1])
    else:
        return np.float32(value)


def clean_string(value):
    """convert string values to float"""

    value = value.replace(",", "")

    return np.float32(value)