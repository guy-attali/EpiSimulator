from core.world import world
from scenarios.scenario1 import setup_world
from metrics.metrics_manager import MetricManager
from display.display_manager import DisplayManager


metrics_interval = 12
display_interval = 12

def main():
    setup_world()

    metrics = MetricManager()
    display = DisplayManager()

    while True:
        if world.current % metrics_interval == 0:
            metrics.show()

        if world.current % display_interval == 0:
            display.update()

        world.tick()

if __name__ == '__main__':
    main()
