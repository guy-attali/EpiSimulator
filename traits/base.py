class Traits():
    def __init__ (self, initial_values):
        for name, value in initial_values.items():
            self[name] = value

    def __getattribute__(self, name):
        if name not in super().__getattribute__("allowed_traits"):
            raise NotImplementedError('unknown trait ' + name)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name not in super().__getattribute__("allowed_traits"):
            raise NotImplementedError('unknown trait ' + name)
        return super().__setattr__(name, value)

    def __setitem__(self, name, value):
        if name not in super().__getattribute__("allowed_traits"):
            raise NotImplementedError('unknown trait ' + name)
        return super().__setattr__(name, value)