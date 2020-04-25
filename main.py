from core.world import world
from scenarios.scenario1 import setup_world
from metrics.metrics_manager import MetricManager

metrics = MetricManager()
metrics_interval = 12

def main():
    setup_world()

    while True:
        if world.current % metrics_interval == 0:
            metrics.show()

        world.tick()

if __name__ == '__main__':
    main()
