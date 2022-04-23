from dash import dcc
from dash import html


# layout
def tab2_layout(selected_companies):
    if selected_companies is None:
        return html.Div(children=[html.Div(["Please select companies to continue"])])
    else:
        return html.Div(children=[html.Div(["Selected companies: " + ", ".join(selected_companies)])])
