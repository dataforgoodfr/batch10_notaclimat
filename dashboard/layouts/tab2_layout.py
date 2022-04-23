from dash import dcc
from dash import html


# layout
def tab2_layout(selected_company):
    return html.Div([
        html.H1('Hello Dash'),
        html.Div([
            html.P('Dash converts Python classes into HTML'),
            html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
        ])
    ])
