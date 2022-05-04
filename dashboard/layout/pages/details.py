from dash import html
from utils import card_style


def details(selected_company):
    return html.Div(children=[html.Div("Détails émissions - " + selected_company, className="h5")],
                    className=card_style)
