from core.world import world
from scenarios.scenario1 import setup_world

def main():
    setup_world()
    world.tick()

if __name__ == '__main__':
    main()
