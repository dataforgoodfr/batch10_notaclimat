# Dash libraries
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Modules
from utils import Pages, isCurrentTab, parse_url, component_ids, state_to_url

# Layouts
from components.navbar import navbar_component, select_company_component
from layout.tab1_layout import tab1_layout
from layout.tab2_layout import tab2_layout

# Style
bootstrap_theme = [dbc.themes.BOOTSTRAP, 'https://use.fontawesome.com/releases/v5.9.0/css/all.css', 'assets/style.css']
app = Dash(external_stylesheets=bootstrap_theme, name="Nota Climat", title="Nota Climat")
server = app.server

# Config
app.config.suppress_callback_exceptions = True

# layout rendu par l'application
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='navbar-select'),
    html.Div(id='navbar-tabs'),
    html.Div(id='page-content', className="overflow-hidden")
],
                      className="d-flex flex-column vh-100")


@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if isCurrentTab(pathname, Pages.COMPANY):
        return html.Div(id='tab-1', className="h-100")
    elif isCurrentTab(pathname, Pages.COMPARE):
        return html.Div(id='tab-2', className="h-100")
    else:
        return html.Div(["404"])


@app.callback(Output('navbar-tabs', 'children'), [Input('url', 'pathname'), Input('url', 'search')])
def display_navbar(pathname, search):
    url_state = parse_url(search)
    return navbar_component(pathname, url_state)


@app.callback(Output('navbar-select', 'children'), [Input('url', 'pathname'), Input('url', 'href')])
def display_nav_select(pathname, href):
    url_state = parse_url(href)
    return select_company_component(pathname, url_state)


@app.callback(Output('tab-1', 'children'), [Input('company_select', 'value')])
def display_tab_1(company_select):
    return tab1_layout(company_select)


@app.callback(Output('tab-2', 'children'), [Input('company_select', 'value')])
def display_tab_2(company_select):
    return tab2_layout(company_select)


@app.callback(Output('url', 'search'), inputs=[Input(i, 'value') for i in component_ids])
def update_url_state(*values):
    return state_to_url(*values)


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
