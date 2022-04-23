# Dash libraries

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from utils import t1b1_df, isCurrentTab, Pages


def select_company_component(currentTab):
    return dcc.Dropdown(
        id='company_select',
        options=[{
            'label': i,
            'value': i
        } for i in t1b1_df['company_name']],
        #value='Andros'
        multi=isCurrentTab(currentTab, Pages.COMPARE),
        searchable=True,
        placeholder='Select a company')


def getNavitemClass(currentTab, tabId):
    return "col" + (' bg-primary' if isCurrentTab(currentTab, tabId) else ' bg-secondary')


def navbar_component(currentTab):
    return html.Div(children=[
        dbc.Navbar(
            [
                dbc.Row(select_company_component(currentTab),
                        class_name="row m-2" + (' w-50' if isCurrentTab(currentTab, Pages.COMPANY) else ' w-50')),
                dbc.Row(
                    [
                        #Navlink accueil
                        dbc.NavItem(dbc.NavLink("Vue entreprise", href="/company", class_name="text-white"),
                                    class_name=getNavitemClass(currentTab, Pages.COMPANY)),
                        #Navlink dashbord
                        dbc.NavItem(dbc.NavLink("Vue comparative", href="/compare", class_name="text-white"),
                                    class_name=getNavitemClass(currentTab, Pages.COMPARE)),
                    ],
                    class_name="row text-center w-100 g-0")
            ],
            class_name="d-flex flex-column align-items-baseline p-0",
            color="dark",
            dark=True,
        )
    ])
