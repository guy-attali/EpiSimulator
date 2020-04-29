from matplotlib import pyplot as plt
from tqdm import tqdm

from core.world import world
from display.display_manager import DisplayManager
from metrics.metrics_manager import MetricManager
from scenarios.scenario1 import Scenario1
from display.plot_connections_graph import plot_connections_graph
from config import gen_params_dict

print_metrics_interval = None
display_interval = None
iters = 1000

metrics = MetricManager()


def main():
    scenario = Scenario1()
    gen_params_dict(scenario.config_file_path)
    world.time_step = scenario.time_step

    scenario.build()

    metrics = MetricManager()
    if display_interval is not None:
        display = DisplayManager()
    for _ in tqdm(range(iters)):
        metrics.add_to_log(log_metrics)
        if print_metrics_interval is not None and \
                world.current % print_metrics_interval == 0:
            metrics.show()

        if display_interval is not None and \
                world.current % display_interval == 0:
            display.update()

        world.tick()

    # plot_connections_graph(metrics.log[:])
    metrics_df = metrics.to_df()
    metrics_df.set_index('time_days')[['s', 'i', 'r']].plot(color=['b', 'r', 'g'])    # plt.legend()
    plt.show()
    1

if __name__ == '__main__':
    main()
