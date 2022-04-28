from dash import html
from utils import card_style


def comments(selected_companies):
    return html.Div(children=[
        html.Div("Commentaires / Méthodologie", className="h3 p-0"),
        html.Hr(),
        html.Div([", ".join(selected_companies)])
    ],
                    className=card_style)
