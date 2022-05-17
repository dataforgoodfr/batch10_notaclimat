from dash import html
from utils import card_style


def sector_compare(selected_company):
    return html.Div(children=[html.Div("Comparaison sectorielle - " + selected_company, className="h5")],
                    className=card_style)
