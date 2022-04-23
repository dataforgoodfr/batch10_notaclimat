# Dash libraries
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# Modules
from utils import Pages, isCurrentTab
from app import app

#import callbacks
from components.navbar import navbar_component
from layouts.tab1_layout import tab1_layout
from layouts.tab2_layout import tab2_layout

# layout rendu par l'application
app.layout = html.Div([dcc.Location(id='url', refresh=True), html.Div(id='navbar'), html.Div(id='page-content')])


@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if isCurrentTab(pathname, Pages.COMPANY):
        return html.Div(id='tab-1')
    elif isCurrentTab(pathname, Pages.COMPARE):
        return html.Div(id='tab-2')
    else:
        return html.Div(id='tab-1')


@app.callback(Output('navbar', 'children'), [Input('url', 'pathname')])
def display_navbar(pathname):
    return navbar_component(pathname)


@app.callback(Output('tab-1', 'children'), Input('company_select', 'value'))
def display_tab_1(company_select):
    return tab1_layout(company_select)


@app.callback(Output('tab-2', 'children'), Input('company_select', 'value'))
def display_tab_2(company_select):
    return tab2_layout(company_select)


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
