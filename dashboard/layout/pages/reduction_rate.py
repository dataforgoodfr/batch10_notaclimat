from dash import html
from utils import card_style


def reduction_rate(selected_companies):
    return html.Div(children=[
        html.Div("Rythmes de réduction des émissions de CO2éq", className="h3 p-0"),
        html.Hr(),
        html.Div([", ".join(selected_companies)])
    ],
                    className=card_style)
