class Plugin:
    def world_pretick(self):
        pass

    def world_posttick(self):
        pass

    def world_post_scenario_build(self):
        pass
    
    def finish(self):
        pass


__all__ = ['Plugin']
