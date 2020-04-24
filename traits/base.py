import abc


class RestrictTraits(abc.ABC):
    """
    A class to restrict attributes for a class. Prohibit only attribute based on a method
    t.d = 4 # AttributeError
    """

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @abc.abstractmethod
    def _attribute_allowed(self, name):
        """
        :param name: The attribute name
        :return: True if should set the attribute, False otherwise
        """
        pass

    def __setattr__(self, name: str, value):
        if not self._attribute_allowed(name) and not name.startswith('_'):  # Allow private attributes
            raise AttributeError("The attribute '{}' isn't allowed".format(name))
        super(RestrictTraits, self).__setattr__(name, value)


PERSON_TRAITS = {'procedures', 'age', 'sex', 'uuid'}
SITE_TRAITS = {'uuid', 'geolocation', 'people', 'log', 'procedures', 'infection_factor', 'dispersion_factor', 'area'}
