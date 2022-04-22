# Dash libraries

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

# Modules

from components.functions import t1b1_df#, t1b1_func

# function

def t1b1_func():
    return html.Div(
	dcc.Dropdown(
	    id='t1b1_div',
	    options=[{'label': i, 'value': i} for i in t1b1_df['company_name']],
	    #value='Andros'
	    multi=False,
	    searchable=True,
	    placeholder='Select a company'
	    )
    )

# layout

tab1_layout = html.Div(children=[t1b1_func()])
