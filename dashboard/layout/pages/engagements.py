from dash import html
from utils import card_style


def engagements(selected_company):
    return html.Div(children=["Engagements - " + selected_company], className=card_style)
