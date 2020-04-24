class ObjectWithAcquiredTraits:
    def __init__(self):
        self._acquired_traits = {}

    def set_trait(self, trait, value):
        if trait in self._acquired_traits:
            self._acquired_traits[trait] = value
        elif trait in self.__dict__:
            self.__dict__[trait] = value
        else:
            raise KeyError

    def get_trait(self, trait):
        return self._acquired_traits.get(trait, default=self.__dict__[trait])

    def has_trait(self, trait):
        return (trait in self._acquired_traits) or (trait in self.__dict__)

    def add_trait(self, trait, value):
        if not self.has_trait(trait):
            self._acquired_traits[trait] = value