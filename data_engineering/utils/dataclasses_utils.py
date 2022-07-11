from dataclasses import dataclass
from pandas import DataFrame


@dataclass(frozen=True)
class RawDataFrames:
    df_companies_data: DataFrame
    df_companies_competitors: DataFrame
    df_global_score: DataFrame
    df_emissions_scope: DataFrame
    df_direct_complete_score: DataFrame
    df_direct_commitment: DataFrame
    df_coeff_director: DataFrame
    df_pos_cursors: DataFrame
    df_marques_by_cat: DataFrame
