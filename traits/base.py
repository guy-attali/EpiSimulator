# traits/__init__.py
# traits/base.py ?
from enum import Enum


class Trait:
    def __init__(self, initial_value=None):
        self.value = initial_value

    def __eq__(self, other):
        if isinstance(other, Trait):
            return self.value is other.value
        return self.value is other

    def __bool__(self):
        return self.value is True


class TRAITTYPE(Enum):
    INFECTED = 1
    SEX = 51
    AGE = 52
