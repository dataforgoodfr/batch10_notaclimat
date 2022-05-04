from dash import html
from utils import card_style


def infos(selected_company):
    return html.Div(children=[html.Div("Infos - " + selected_company, className="h5")], className=card_style)
