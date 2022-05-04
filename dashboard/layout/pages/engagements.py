from dash import html
from utils import card_style


def engagements(selected_company):
    return html.Div(children=[html.Div("Engagements - " + selected_company, className="h5")], className=card_style)
