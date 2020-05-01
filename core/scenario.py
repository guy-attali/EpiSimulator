import abc


class ScenarioBase(abc.ABC):
    @abc.abstractmethod
    def build(self):
        pass
