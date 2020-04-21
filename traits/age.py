from traits.base import TRAITTYPE, Trait


class TraitAge(Trait):
    c = TRAITTYPE.AGE

    def __init__(self, age: int):
        super(TraitAge, self).__init__(age)

    def within(self, start, end):
        return start < self.value < end
