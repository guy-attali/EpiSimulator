import yaml
params_dict = {}


def gen_params_dict(config_file_path):
    with open(config_file_path) as f:
        params_dict.update(yaml.load(f, Loader=yaml.FullLoader))
