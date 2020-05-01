import sys, yaml


def extend_from_dict(options):
    sys.modules[__name__].__dict__.update(options)

def extend_from_filename(filename):
    with open(filename) as f:
        sys.modules[__name__].__dict__.update(yaml.load(f, Loader=yaml.FullLoader))
