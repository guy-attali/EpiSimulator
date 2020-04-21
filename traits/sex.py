from enum import Enum

from traits.abstract import Trait, TRAITTYPE


class SEX(Enum):
    MALE = 0
    FEMALE = 1


class TraitSex(Trait):
    c = TRAITTYPE.SEX

    def __init__(self, sex: SEX):
        super(TraitSex, self).__init__(sex)
