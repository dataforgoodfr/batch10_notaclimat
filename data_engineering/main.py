from data_engineering.configs.config import Config
from data_engineering.data_retrieving.spreadsheet_data_reader import read_raw_data
from data_engineering.connecting.google_spreadsheet_connector import get_google_spreadsheet_connection
from data_engineering.data_wrangling.data_wrangler import wrangle_data
from data_engineering.data_writing.spreadsheet_writer import write_to_spreadsheet

config = Config()

spreadsheet_connector = get_google_spreadsheet_connection(service_account_json_key=config.paths.gcp_key)
raw_data = read_raw_data(service=spreadsheet_connector,
                         spreadsheet_id=config.spreadsheet.raw_data_spreadsheet_id,
                         list_groups_wanted=config.data_processing.list_groups_wanted)
final_data = wrangle_data(raw_dataframes=raw_data, list_groups=config.data_processing.list_groups_wanted)
write_to_spreadsheet(dataframe_to_write=final_data, spreadsheet_client=spreadsheet_connector,
                     spreadsheet_id=config.spreadsheet.processed_data_spreadsheet_id,
                     spreadsheet_range=config.spreadsheet.processed_data_spreadsheet_range)
