import argparse
from data_engineering.configs.config_parser import read_config_from_json
import logging
from dotmap import DotMap

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def get_config() -> DotMap:
    args = None
    try:
        args = get_args()
    except:
        logger.error("missing or invalid arguments")
        exit(0)
    config = read_config_from_json(args.conf)
    return config


def get_args():
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument(
        '--conf',
        '-c',
        type=str,
        required=True,
        help='path to configs json file')
    args = arg_parser.parse_args()
    return args


