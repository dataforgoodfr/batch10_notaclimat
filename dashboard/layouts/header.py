# Dash libraries

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from components.utils import t1b1_df, isCurrentTab


def select_company_component():
    return dcc.Dropdown(
        id='company_select',
        options=[{
            'label': i,
            'value': i
        } for i in t1b1_df['company_name']],
        #value='Andros'
        multi=False,
        searchable=True,
        placeholder='Select a company')


def getNavitemClass(currentTab, tabId):
    return "col" + (' bg-primary' if isCurrentTab(currentTab, tabId) else ' bg-secondary')


def navbar_component(pathname):
    return html.Div(children=[
        dbc.Navbar(
            [
                dbc.Row(select_company_component(), class_name="row w-25 m-2"),
                dbc.Row(
                    [
                        #Navlink accueil
                        dbc.NavItem(dbc.NavLink("Vue entreprise", href="/company", class_name="text-white"),
                                    class_name=getNavitemClass(pathname, 'company')),
                        #Navlink dashbord
                        dbc.NavItem(dbc.NavLink("Vue comparative", href="/compare", class_name="text-white"),
                                    class_name=getNavitemClass(pathname, 'compare')),
                    ],
                    class_name="row text-center w-100 g-0")
            ],
            class_name="d-flex flex-column align-items-baseline p-0",
            color="dark",
            dark=True,
        )
    ])
