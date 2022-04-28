from dash import html
from utils import card_style


def action_suivi(selected_company):
    return html.Div(children=["Action actuelle - " + selected_company], className=card_style)
