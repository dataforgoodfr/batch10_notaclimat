# Dash libraries

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

# Modules

from components.functions import t1b1_df
import components.functions

# test

tab2_layout = html.Div([
    html.H1('Hello Dash'),
    html.Div([
	html.P('Dash converts Python classes into HTML'),
	html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
    ])
])
