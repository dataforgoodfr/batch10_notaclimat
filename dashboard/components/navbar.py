# Dash libraries

import ast
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from utils import t1b1_df, isCurrentTab, Pages, component_ids, state_to_url


def select_company_component(currentTab, state):
    default_value = state[component_ids[0]] if len(state) >= 1 else None

    if default_value is not None and default_value[0] == '[':
        default_value = ast.literal_eval(default_value)

    if isCurrentTab(currentTab, Pages.COMPARE) and default_value is not None and type(default_value) is not list:
        default_value = [default_value]

    return html.Div(
        children=[
            html.Div([
                html.Div([
                    html.Img(src="/assets/Pics/nav_logo.png", className="h-100 p-2"),
                    html.A("Accueil",
                           className="text-decoration-none text-primary fs-5 ms-4",
                           href="https://notaclimat.com/")
                ],
                         className="d-flex align-items-center h-100"),
                html.A("Ajouter les données d'une entreprise",
                       className="bg-primary btn d-block px-3 py-2 rounded-2 text-decoration-none text-white",
                       href="https://notaclimat.com/new_data")
            ],
                     className="d-flex h-12 bg-white align-items-center justify-content-between px-4",
                     style={"height": '65px'}),
            dcc.Dropdown(
                id='company_select',
                options=[{
                    'label': i,
                    'value': i
                } for i in t1b1_df['company_name']],
                #value='Andros'
                multi=isCurrentTab(currentTab, Pages.COMPARE),
                searchable=True,
                #placeholder='Select a company', #English version
                placeholder='Sélectionnez une société', #French version                
                value=(default_value),
                className=(' w-98' if isCurrentTab(currentTab, Pages.COMPANY) else ' w-98') + " mx-2 mt-2 mb-1"),
        ],
        className="bg-primary w-100 pb-2")


def getNavitemClass(currentTab, tabId):
    return "col" + (' bg-primary' if isCurrentTab(currentTab, tabId) else '')


def getHref(link, state):
    select_value = state[component_ids[0]] if len(state) >= 1 else None

    if select_value is not None and select_value[0] == '[':
        select_value = ast.literal_eval(select_value)

    if select_value is None:
        return "/" + link.value

    search = ""

    if link == Pages.COMPANY:
        if type(select_value) is list:
            search = state_to_url(select_value[0])
        else:
            search = state_to_url(select_value)
    elif link == Pages.COMPARE:
        if type(select_value) is list:
            search = state_to_url(select_value)
        else:
            search = state_to_url([select_value])

    return "/" + link.value + search


def navbar_component(currentTab, *current_values):
    return html.Div(children=[
        dbc.Navbar(
            [
                dbc.Row(
                    [
                        #Navlink accueil
                        dbc.NavItem(dbc.NavLink("Vue entreprise",
                                                href=getHref(Pages.COMPANY, *current_values),
                                                class_name="h5 text-white my-1"),
                                    class_name=getNavitemClass(currentTab, Pages.COMPANY)),
                        #Navlink dashboard
                        dbc.NavItem(dbc.NavLink("Vue comparative",
                                                href=getHref(Pages.COMPARE, *current_values),
                                                class_name="h5 text-white my-1"),
                                    class_name=getNavitemClass(currentTab, Pages.COMPARE)),
                    ],
                    class_name="row text-center w-100 g-0")
            ],
            class_name="d-flex flex-column align-items-baseline p-0",
            color="dark",
            dark=True,
        )
    ])
