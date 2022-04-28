from dash import html
from utils import card_style


def sector_compare(selected_company):
    return html.Div(children=["Comparaison sectorielle - " + selected_company], className=card_style)
