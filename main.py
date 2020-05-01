#!/usr/bin/python

import os, sys, getopt, config, argparse, importlib
from core.world import world

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

def main():
  parser = argparse.ArgumentParser(description='Execute a simulation scenario')
  parser.add_argument('scenario', metavar='scenario',
                      help='Named scenario in scenarios directory')

  parser.add_argument('-c', dest='config_filename', metavar='config_filename', help='Alternative configuration filename', default=os.path.join(root_path, 'config.yml'))
  parser.add_argument('-v', dest='verbose', action='store_true')
  parser.add_argument('-p', dest='pipe_log')
  parser.add_argument('-t', dest='ticks', type=int, default=1)

  args = parser.parse_args()


  config.extend_from_filename(args.config_filename)
  config.extend_from_dict({ "verbose": args.verbose })

  spec = importlib.util.find_spec('scenarios.' + args.scenario)

  if spec is None:
    print('Unknown scenario: ' + args.scenario)
    sys.exit()

  scenario_module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(scenario_module)
  scenario = scenario_module.Scenario()

  world.run_scenario(scenario)
  for _ in range(args.ticks):
      world.tick()


if __name__ == '__main__':
    main()