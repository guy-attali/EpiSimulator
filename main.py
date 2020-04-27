
from core.world import world
from display.display_manager import DisplayManager
from metrics.metrics_manager import MetricManager
from scenarios.scenario1 import Scenario1
from display.plot_connections_graph import plot_connections_graph

from datetime import timedelta

from config import gen_params_dict
gen_params_dict()
world.time_step = timedelta(minutes=120)

print_metrics_interval = 1
display_interval = 1000
iters = 1000


metrics = MetricManager()



def main():
    scenario = Scenario1()
    scenario.build()

    metrics = MetricManager()
    display = DisplayManager()

    for _ in range(iters):
        metrics.add_to_log()
        if world.current % print_metrics_interval == 0:
            metrics.show()

        if world.current % display_interval == 0:
            display.update()

        world.tick()

    plot_connections_graph(metrics.log[:])
    metrics_df = metrics.to_df()
    metrics_df.set_index('time_days')[['s', 'i', 'r']].plot(color=['b', 'r', 'g'])    # plt.legend()
    1

if __name__ == '__main__':
    main()
