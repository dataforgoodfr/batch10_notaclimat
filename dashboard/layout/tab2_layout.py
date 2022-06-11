from dash import html

from layout.pages.reduction_rate import reduction_rate
from layout.pages.comments import comments


# layout
def tab2_layout(selected_companies):
    if selected_companies is None or type(selected_companies) is not list or len(selected_companies) == 0:
        return html.Div(children=[
            html.Div(["Sélectionnez au moins deux sociétés pour continuer"], className="h2 w-100 p-3 text-center")
        ])

    return html.Div(children=[
        html.Div(children=[
            reduction_rate(selected_companies),
        ], className="row gap-2 w-100"),
        html.Div(children=[comments(selected_companies)], className="row gap-2 w-100")
    ],
                    className="container-fluid row py-3 gap-3 m-0 h-100 overflow-auto w-100")
