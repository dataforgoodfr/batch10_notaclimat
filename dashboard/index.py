# Dash libraries

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Modules

import callbacks
from layouts.header import navbar
from layouts.tab1_layout import tab1_layout
from layouts.tab2_layout import tab2_layout
from app import app,server

# layout rendu par l'application

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    navbar,
    html.Div(id='page-content')
])

# callback pour mettre à jour les pages

@app.callback(Output('page-content', 'children'),
	      [Input('url', 'pathname')])
def display_page(pathname):
	if pathname=='/tab1' or pathname=='/':
		return tab1_layout
	elif pathname=='/tab2':
		return tab2_layout
if __name__ == '__main__':
	app.run_server(debug=True)
