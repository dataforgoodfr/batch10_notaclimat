from dash import html

from layout.pages.engagements import engagements
from layout.pages.infos import infos
from layout.pages.details import details
from layout.pages.action_suivi import action_suivi
from layout.pages.sector_compare import sector_compare


# layout
def tab1_layout(selected_company):
    if selected_company is None:
        return html.Div(children=[html.Div(["Please select a company to continue"])])
    elif type(selected_company) is list:
        selected_company = selected_company[0]

    return html.Div(children=[
        html.Div(children=[
            infos(selected_company),
            engagements(selected_company),
            details(selected_company),
        ],
                 className="col-3 d-flex flex-column gap-2"),
        html.Div(
            children=[
                action_suivi(selected_company),
                sector_compare(selected_company)
            ],
            className="col d-flex flex-column gap-2"
        )
    ],
                    className="container-fluid row py-3 gap-3 m-0 h-100 flex-nowrap")
