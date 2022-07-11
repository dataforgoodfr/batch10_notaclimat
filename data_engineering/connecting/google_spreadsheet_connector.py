from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging
import os
import pandas as pd
from typing import Union

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def get_google_spreadsheet_connection(service_account_json_key) -> object:
    f"""
        get a google spreadsheet api resource

        :return:    a Resource object that connects to the google spreadsheet api. 
        """
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    _service_account_json_key = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') if os.environ.get(
        'GOOGLE_APPLICATION_CREDENTIALS') else service_account_json_key
    credentials = service_account.Credentials.from_service_account_file(filename=_service_account_json_key,
                                                                        scopes=scope)
    service = build(
        'sheets',
        'v4',
        credentials=credentials,
        cache_discovery=False
    ).spreadsheets()

    logger.info("google spreadsheet connection established successfully !")

    return service

