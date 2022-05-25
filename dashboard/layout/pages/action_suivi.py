from dash import html
from utils import card_style, t1b3_df

from layout.pages.action_suivi_global import action_suivi_global
from layout.pages.action_suivi_actuel import action_suivi_actuel

def action_suivi(selected_company):
    return html.Div(
        children=[
            action_suivi_actuel(selected_company),
            action_suivi_global(selected_company)        
        ],
        className=card_style
    )
