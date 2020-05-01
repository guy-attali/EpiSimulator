import os, config
from tqdm import tqdm
from policies.matplot import PolicyMatplot
from policies.pandas import PolicyPandas
from core.world import world


SECONDS_IN_DAY = 60 * 60 * 24
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
config.extend_from_filename(os.path.join(ROOT_PATH, 'config.yml'))


def run_scenario(Scenario, print_metrics_interval=None, display_interval=None,
                    iters=10, sim_days=None, config_ext={}):

    config.extend_from_dict(config_ext)
    world.reset()

    policy_pandas = PolicyPandas(print_metrics_interval)
    world.append_policy(policy_pandas)

    if display_interval is not None:
        policy_matplot = PolicyMatplot(display_interval)
        world.append_policy(policy_matplot)

    scenario = Scenario()
    world.run_scenario(scenario)

    if sim_days is not None:
        iters = int(sim_days * SECONDS_IN_DAY / scenario.time_step.total_seconds())
    

    for _ in tqdm(range(iters)):
        world.tick()
    
    world.finish()

    return {
        'policy_pandas': policy_pandas,
        'policy_matplot': policy_matplot
    }
