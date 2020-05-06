from core.world import world
from display.display_manager import DisplayManager
from metrics.metrics_manager import MetricManager
from config import gen_params_dict
from tqdm import tqdm

SECONDS_IN_DAY = 60 * 60 * 24


def scenario_runner(scenario, print_metrics_interval=None, display_interval=None,
                    iters=1000, sim_days=None, log_metrics=None):
    world.__init__()
    gen_params_dict(scenario.config_file_path)
    world.time_step = scenario.time_step
    if sim_days is not None:
        iters = int(sim_days * SECONDS_IN_DAY / scenario.time_step.total_seconds())

    scenario.build()
    metrics = MetricManager()
    if display_interval is not None:
        display = DisplayManager()
    for _ in tqdm(range(iters)):
        metrics.add_to_log(log_metrics=log_metrics)
        # print(world.current_time, world.people[0].site.name)
        if print_metrics_interval is not None and \
                world.current % print_metrics_interval == 0:
            metrics.show()

        if display_interval is not None and \
                world.current % display_interval == 0:
            display.update()

        world.tick()

    return metrics
