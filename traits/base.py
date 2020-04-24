from typing import List, Optional


class Traits:
    """
    This class represents a dict access using attributes instead of items, and restricting attributes using a
    given list. For example:

    t = Traits(allowed_traits=['a', 'b'], c=3) # Initiating allowed traits in c'tor, based on allowed_traits and kwargs
    t.a = t.c - 2 # fine
    t.d = 4 # AttributeError
    """

    def __init__(self, allowed_traits: Optional[List[str]] = None, **kwargs):
        allowed_traits = allowed_traits or []
        self.__dict__['_allowed_traits'] = allowed_traits
        self.__dict__['_traits_dict'] = {}
        for key in kwargs:
            self._allowed_traits.append(key)
            setattr(self, key, kwargs[key])

    def __getattr__(self, item):
        # Not checking ALLOWED_TRAITS as it checked in setattr
        if item not in self._traits_dict:
            raise AttributeError("No such attribute '{}'".format(item))
        return self._traits_dict[item]

    def __setattr__(self, name, value):
        if name not in self._allowed_traits:
            raise AttributeError("The attribute '{}' isn't allowed".format(name))
        self._traits_dict[name] = value
