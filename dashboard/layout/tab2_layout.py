from dash import html

from layout.pages.reduction_rate import reduction_rate
from layout.pages.comments import comments


# layout
def tab2_layout(selected_companies):
    if selected_companies is None or type(selected_companies) is not list or len(selected_companies) == 0:
        return html.Div(children=[html.Div(["Please select companies to continue"])])

    return html.Div(children=[
        html.Div(children=[
            reduction_rate(selected_companies),
        ], className="row gap-2"),
        html.Div(children=[comments(selected_companies)], className="row gap-2")
    ],
                    className="container-fluid row pt-3 gap-3 m-0")
