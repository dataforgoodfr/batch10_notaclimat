from dash import html
from utils import card_style


def infos(selected_company):
    return html.Div(children=["Infos - " + selected_company], className=card_style)
