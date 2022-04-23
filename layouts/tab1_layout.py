from dash import dcc
from dash import html


# layout
def tab1_layout(selected_company):
    if selected_company is None:
        return html.Div(children=[html.Div(["Please select a company to continue"])])
    else:
        return html.Div(children=[html.Div(["Selected company: " + selected_company])])
