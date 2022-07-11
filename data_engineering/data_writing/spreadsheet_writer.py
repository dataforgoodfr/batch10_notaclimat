import pandas as pd
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def write_to_spreadsheet(dataframe_to_write: pd.DataFrame,
                         spreadsheet_client,
                         spreadsheet_id: str,
                         spreadsheet_range: str) -> None:
    f"""
    write a dataframe into a google spreadsheet

    :param spreadsheet_id: id of the google spreadsheet
    :param spreadsheet_client : spreadsheet resource instantiated
    :param dataframe_to_write: dataframe that needs to be written to google spreadsheet
    :param spreadsheet_range: range where the data needs to be written in the A1 notation (sheet + cell, see documentation here : https://developers.google.com/sheets/api/guides/concepts#cell) 

    :return: None
    """
    logger.info(f"writing into spreadsheet {spreadsheet_id}...")
    data_to_write = dataframe_to_write.T.reset_index().values.T.tolist()
    logger.info(f"clearing sheet for range {spreadsheet_range}...")
    spreadsheet_client.values().clear(spreadsheetId=spreadsheet_id,
                                      range=spreadsheet_range).execute()

    spreadsheet_client.values().update(spreadsheetId=spreadsheet_id,
                                       range=spreadsheet_range,
                                       valueInputOption="USER_ENTERED",
                                       body={"values": data_to_write}).execute()

    logger.info(f"data has been written into spreadsheet {spreadsheet_id} with success !")
