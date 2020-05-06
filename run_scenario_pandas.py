import config
import os

from tqdm import tqdm

from core.world import world
from plugins.matplot import PluginMatplot
from plugins.pandas import PluginPandas

SECONDS_IN_DAY = 60 * 60 * 24
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
config.extend_from_filename(os.path.join(ROOT_PATH, 'config.yml'))


def run_scenario(Scenario, print_metrics_interval=None, display_interval=None,
                 iters=10, sim_days=None, config_ext={}):
    config.extend_from_dict(config_ext)
    world.reset()

    plugin_pandas = PluginPandas(print_metrics_interval)
    world.append_plugin(plugin_pandas)

    if display_interval is not None:
        plugin_matplot = PluginMatplot(display_interval)
        world.append_plugin(plugin_matplot)

    scenario = Scenario()
    world.run_scenario(scenario)

    if sim_days is not None:
        iters = int(sim_days * SECONDS_IN_DAY / scenario.time_step.total_seconds())

    for _ in tqdm(range(iters)):
        world.tick()

    world.finish()

    return {
        'pandas': plugin_pandas,
        'matplot': plugin_matplot
    }
