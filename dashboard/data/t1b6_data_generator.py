import pandas as pd
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px


# Read file
df_bdd_surcouche = pd.read_csv(
    'BDD Surcouche modif.csv', 
    header=0,
    sep=';'
)


# Transform DataFrame
df_t1b6 = df_bdd_surcouche.copy()


## Rename Group to company_name
df_t1b6 = df_t1b6.rename({'Group':'company_name'}, axis=1)


## Change amount type (from percentage to float - for example 0.1)
df_t1b6.loc[:, [col for col in df_t1b6.columns if 'amount' in col]] = df_t1b6.loc[:, [col for col in df_t1b6.columns if 'amount' in col]].apply(lambda x: x.str[:-1].astype(int)).astype(int)/100

## Concatenate amount, name and hover values in a single column
cols = ['emissions_category1_amount', 'emissions_category2_amount', 'emissions_category3_amount', 'emissions_category4_amount', 'emissions_category5_amount', 'emissions_category6_amount']
df_t1b6['emissions_category_amount'] = df_t1b6[cols].apply(lambda row: ','.join(row.values.astype(str)), axis=1)

cols = ['emissions_category1_name', 'emissions_category2_name', 'emissions_category3_name', 'emissions_category4_name', 'emissions_category5_name', 'emissions_category6_name']
df_t1b6['emissions_category_name'] = df_t1b6[cols].apply(lambda row: ','.join(row.values.astype(str)), axis=1)

cols = ['emissions_category1_hover', 'emissions_category2_hover', 'emissions_category3_hover', 'emissions_category4_hover', 'emissions_category5_hover', 'emissions_category6_hover']
df_t1b6['emissions_category_hover'] = df_t1b6[cols].apply(lambda row: ','.join(row.values.astype(str)), axis=1)


## Keep useful columns
df_t1b6 = df_t1b6[
    ['company_name',
    'total_emissions', 
    'total_emissions_year',
    'emissions_category_name',
    'emissions_category_amount',
    'emissions_category_hover']
    ]


# Write output file
df_t1b6.to_csv(
    path_or_buf='t1b6.csv', 
    sep=';', 
    header=True, 
    index=False
)