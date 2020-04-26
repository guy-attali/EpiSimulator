import abc


class Scenario(abc.ABC):
    @abc.abstractmethod
    def build(self):
        pass
