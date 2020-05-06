import abc


class Plugin(abc.ABC):
    @abc.abstractmethod
    def world_pretick(self):
        pass

    @abc.abstractmethod
    def world_posttick(self):
        pass

    @abc.abstractmethod
    def world_post_scenario_build(self):
        pass

    @abc.abstractmethod
    def finish(self):
        pass


__all__ = ['Plugin']
