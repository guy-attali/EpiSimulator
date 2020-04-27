import yaml
params_dict = {}

def gen_params_dict():
    with open('config.yml') as f:
        params_dict.update(yaml.load(f, Loader=yaml.FullLoader))
