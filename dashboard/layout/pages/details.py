from dash import html
from utils import card_style


def details(selected_company):
    return html.Div(children=["Détails émissions - " + selected_company], className=card_style)
