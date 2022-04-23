# Dash libraries

import dash
import dash_bootstrap_components as dbc
from dash import html

# Code to explicit

LOGO = "https://i2.wp.com/ledatascientist.com/wp-content/uploads/2019/01/31934826_632207023790117_7976915477504983040_o.png?fit=1638%2C1638&ssl=1"

navbar = dbc.Navbar(
    [
        html.Div(
            # Alignement vertical de l'image et de l'acceuil
            dbc.Row(
                [  #logo
                    dbc.Col(html.Img(src=LOGO, height="40px")),
                    #Navlink Acceuil
                    dbc.NavLink("Vue entreprise", href="/tab1", style={'color': 'white'}),
                    #Navlink dashbord
                    dbc.NavLink("Vue comparative", href="/tab2", style={'color': 'white'})
                ],
                align="center",
                className="g-0",
            ), ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="dark",
    dark=True,
)
