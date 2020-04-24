from traits.base import PERSON_TRAIT_TYPE, Trait


class TraitAge(Trait):
    c = PERSON_TRAIT_TYPE.AGE

    def __init__(self, age: int):
        super(TraitAge, self).__init__(age)

    def within(self, start, end):
        return start <= self.value < end
