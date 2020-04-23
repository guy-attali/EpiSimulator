from enum import Enum

from traits.base import Trait, PERSON_TRAIT_TYPE


class SEX(Enum):
    MALE = 0
    FEMALE = 1


class TraitSex(Trait):
    c = PERSON_TRAIT_TYPE.SEX

    def __init__(self, sex: SEX):
        super(TraitSex, self).__init__(sex)
