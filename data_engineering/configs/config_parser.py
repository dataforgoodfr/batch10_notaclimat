import json
from dotmap import DotMap


def read_config_from_json(json_file) -> DotMap:
    """
    Get the configs from a json file
    :param json_file:
    :return: configs(namespace) or configs(dictionary)
    """
    with open(json_file, 'r') as config_file:
        config_dict = json.load(config_file)

    config: DotMap = DotMap(config_dict)

    return config
