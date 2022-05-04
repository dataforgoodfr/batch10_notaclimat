import pandas as pd
import numpy as np
import os
# import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px


# Path
path = os.path.dirname(__file__)


# Read file
df_bdd_surcouche = pd.read_csv(
    path + '\\Data\\BDD Surcouche modif.csv', 
    header=0,
    sep=';'
)


# Keep useful columns for the block
df_emissions_details = df_bdd_surcouche.loc[:,
    [col for col in df_bdd_surcouche.columns if 
        ('Group' in col)|
        ('total_emissions' in col)|
        ('name' in col)|
        ('amount' in col)|
        ('hover' in col)
    ]
]


# Transform DataFrame
df_emissions_details_amount = df_emissions_details.melt(
    id_vars=['Group', 'total_emissions'],
    value_vars=[col for col in df_bdd_surcouche.columns if 
        ('amount' in col)
    ],
    var_name='Category_number',
    value_name='Amount'
)
df_emissions_details_amount['Category_number'] = df_emissions_details_amount[
    'Category_number'].str.split('_', expand=True)[1]

df_emissions_details_cat_name = df_emissions_details.melt(
    id_vars=['Group'],
    value_vars=[col for col in df_bdd_surcouche.columns if 
        ('name' in col)
    ],
    var_name='Category_number',
    value_name='Category'
)
df_emissions_details_cat_name['Category_number'] = df_emissions_details_cat_name[
    'Category_number'].str.split('_', expand=True)[1]

df_emissions_details_hover = df_emissions_details.melt(
    id_vars=['Group'],
    value_vars=[col for col in df_bdd_surcouche.columns if 
        ('hover' in col)
    ],
    var_name='Category_number',
    value_name='Hover'
)
df_emissions_details_hover['Category_number'] = df_emissions_details_hover['Category_number'].str.split(
    '_', expand=True)[1]

df_emissions_details = df_emissions_details_amount.merge(
    df_emissions_details_cat_name, how='outer').merge(
        df_emissions_details_hover, how='outer'
    )


# Convert Amount from percentage to absolute value
df_emissions_details['Amount'] = df_emissions_details['Amount'].str[:-1].astype(int) / 100
df_emissions_details['Amount'] = df_emissions_details['Amount']*df_emissions_details['total_emissions']
df_emissions_details['Amount'] = df_emissions_details['Amount'].astype(int)


# Sort by Group name and category
df_emissions_details = df_emissions_details.sort_values(['Group', 'Category_number'], ignore_index=True)


# Write output file
df_emissions_details.to_csv(
    path_or_buf='t1b6.csv', 
    sep=';', 
    header=True, 
    index=False
)