from dotmap import DotMap
from dataclasses import dataclass
from data_engineering.configs.config_getter import get_config


class Config(object):
    config: DotMap = get_config()

    @dataclass(frozen=True)
    class Paths:
        gcp_key: str

    @dataclass(frozen=True)
    class Spreadsheet:
        raw_data_spreadsheet_id: str
        processed_data_spreadsheet_id: str
        processed_data_spreadsheet_range: str

    @dataclass(frozen=True)
    class DataProcessing:
        list_groups_wanted: list

    spreadsheet = Spreadsheet(raw_data_spreadsheet_id=config.spreadsheet.raw_data_spreadsheet_id,
                              processed_data_spreadsheet_id=config.spreadsheet.processed_data_spreadsheet_id,
                              processed_data_spreadsheet_range=config.spreadsheet.processed_data_spreadsheet_range)

    paths = Paths(gcp_key=config.paths.gcp_key)

    data_processing = DataProcessing(list_groups_wanted=config.data_processing.list_groups_wanted)
