import logging
import pandas as pd
from typing import Union
from data_engineering.utils.dataclasses_utils import RawDataFrames

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def read_spreadsheet_into_pandas(service: object,
                                 spreadsheet_id: str,
                                 spreadsheet_range: str) -> Union[pd.DataFrame, None]:
    # Call the Sheets API
    result = service.values().get(spreadsheetId=spreadsheet_id,
                                  range=spreadsheet_range).execute()
    values = result.get('values', [])
    return pd.DataFrame(values[1:], columns=values[0])


def read_raw_data(service: object, spreadsheet_id: str, list_groups_wanted: list) -> RawDataFrames:
    df_companies_data = read_spreadsheet_into_pandas(service=service, spreadsheet_id=spreadsheet_id,
                                                     spreadsheet_range='Companies data')
    df_companies_data_final = df_companies_data.copy(deep=True)
    df_companies_data_final = df_companies_data_final[df_companies_data_final["Group"].isin(list_groups_wanted)]

    df_companies_competitors = read_spreadsheet_into_pandas(service=service, spreadsheet_id=spreadsheet_id,
                                                            spreadsheet_range='Companies competitors')
    df_global_score = read_spreadsheet_into_pandas(service=service, spreadsheet_id=spreadsheet_id,
                                                   spreadsheet_range='Global score display')
    df_emissions_scope = read_spreadsheet_into_pandas(service=service, spreadsheet_id=spreadsheet_id,
                                                      spreadsheet_range='Emissions scopes description')
    df_direct_complete_score = read_spreadsheet_into_pandas(service=service, spreadsheet_id=spreadsheet_id,
                                                            spreadsheet_range='Direct and complete score display')
    df_direct_commitment = read_spreadsheet_into_pandas(service=service, spreadsheet_id=spreadsheet_id,
                                                        spreadsheet_range='Direct and complete commitment display')
    df_coeff_director = read_spreadsheet_into_pandas(service=service, spreadsheet_id=spreadsheet_id,
                                                     spreadsheet_range='Coeff directeur pour graph')
    df_pos_cursors = read_spreadsheet_into_pandas(service=service, spreadsheet_id=spreadsheet_id,
                                                  spreadsheet_range='Positionnement des curseurs')
    df_marques_by_cat = read_spreadsheet_into_pandas(service=service, spreadsheet_id=spreadsheet_id,
                                                     spreadsheet_range='Table Marques par catégorie')
    logger.info("google spreadsheet values retrieved successfully !")

    return RawDataFrames(df_companies_data=df_companies_data_final,
                         df_companies_competitors=df_companies_competitors,
                         df_global_score=df_global_score,
                         df_emissions_scope=df_emissions_scope,
                         df_direct_complete_score=df_direct_complete_score,
                         df_direct_commitment=df_direct_commitment,
                         df_coeff_director=df_coeff_director,
                         df_pos_cursors=df_pos_cursors,
                         df_marques_by_cat=df_marques_by_cat)
