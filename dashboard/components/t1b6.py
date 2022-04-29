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


# Reading file
df_bdd_surcouche = pd.read_csv(
    path + '\\Data\\BDD Surcouche pour dataviz_v03.xlsx - Table Dash - Vue 1 entreprise.csv', 
    header=0,
    skiprows=[1]
)


# Keep useful columns for the block
df_emissions_details = df_bdd_surcouche.loc[:, [col for col in df_bdd_surcouche.columns if 
    ('Group' in col)|('Tota emissions' in col)|('Cat' in col)|('Wording interactive' in col)
]]


# Collecting useful data for the chart
group = 'Bel'
df_emissions_details = df_emissions_details[df_emissions_details['Group']==group]

## Total emissions for the center hole
total = df_emissions_details.loc[1, 'Tota emissions']

## Name of categories
cat_names = df_emissions_details.loc[1, [
    col for col in df_bdd_surcouche.columns if 'name' in col
    ]
]
cat_names.index = cat_names.index.str[:-5]

## Emissions amount for each category
amount = df_emissions_details.loc[1, [
    col for col in df_bdd_surcouche.columns if 'amount' in col
    ]
]
amount = amount.str[:-1].astype(int)
amount = amount*total / 100
amount = amount.astype(int)
amount.index = amount.index.str[:-7]

## Hover text for each category
description = df_emissions_details.loc[1, [
    col for col in df_bdd_surcouche.columns if 'Wording interactive' in col
    ]
]
description.index = [('Cat ' + str(i)) for i in description.index.str[-1:]]

## Creating df_graph with data for the graph
df_graph = pd.concat([cat_names, amount, description], axis=1)
df_graph.columns = ['Category', 'Amount', 'Description']


# Generating chart
fig = px.pie(
    df_graph,
    values='Amount',
    names='Category',
    # title='Details of emissions by category',
    hover_data=['Description']
)
fig.update_traces(textposition='inside', hole=.4, textinfo='label+percent', insidetextorientation='radial')
fig.update_layout(
    showlegend=False,
    annotations=[dict(text=('Total <br>' + str(total) + ' tCO2eq'), x=0.50, y=0.5, font_size=12, showarrow=False)]
)
fig.show()