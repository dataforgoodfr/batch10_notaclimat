# Dash libraries

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import html
import dash_table

# Modules

from components.functions import df_pc

# Datetime libraries

from datetime import date, timedelta

from datetime import datetime as dt

# Code to explicit

######################## START Log action sur site ########################
LOGO = "https://i2.wp.com/ledatascientist.com/wp-content/uploads/2019/01/31934826_632207023790117_7976915477504983040_o.png?fit=1638%2C1638&ssl=1"
html.Img(src=LOGO, height="40px")

current_year_df_pc, month, day, hour, min = map(int,df_pc.dates.max().strftime("%Y %m %d %H %M").split())
date_picker=dcc.DatePickerRange(
  id='my-date-picker-range-publishing',
  # with_portal=True,
  min_date_allowed=(df_pc['dates'].max()-timedelta(60)).to_pydatetime(),
  max_date_allowed=df_pc['dates'].max().to_pydatetime(),
  initial_visible_month=dt(current_year_df_pc,df_pc['dates'].max().to_pydatetime().month, 1),
  start_date=(df_pc['dates'].max() - timedelta(28)).date(),
  end_date=df_pc['dates'].max().date(),
  #style={'marginLeft': 100}
)


table = dash_table.DataTable(

     id='table',
     columns=[{"name": i, "id": i, 'deletable': True} for i in df_pc.columns.to_list()],
     editable=True,
     #n_fixed_columns=2,
     style_table={'maxWidth': '1500px'},
     row_selectable="multi",
     selected_rows=[0],
     style_cell = {"fontFamily": "Arial", "size": 10, 'textAlign': 'center', 'color':'dark'},
     css=[{'selector': '.dash-cell div.dash-cell-value', 'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],

 )


body = dbc.Container([
        html.Br(),
        dbc.Row(
                [
                dbc.Col(

                    html.Div(
                        [   html.Br([]),
                            html.H5("Bienvenue!",style={'color':'red','backgroundColor':'white'}),
                            html.Br([]),
                            html.P(
                                "\
                            Vous êtes sur la page d'acceuil du tutoriel de développement de dashbord en python avec Dash. \
                            Je vous présente ici les données du trafic web d'un site internet. Ce sont notamment les accès avec  \
                            differents appareils (mac, android, iphone_ipad, autre_pc) que vous pouvez visualiser ici sur\
                            2 mois (Octobre - novembre) grâce à un sélecteur de date dans la table ci-dessous.",

                                style={"color": "#000406"},

                            ),
                            html.P(
                                "\
                            Ces données ont par la suite été transformées pour interagir dynamiquement avec des graphiques. \
                            On y affiche des informations telles que: le nombre total d'accès à la plateform par appareil ,  \
                        les graphiques d'évolution des accès par appareil , par type d'appareil et par système d'exploitation sur plusieurs mois et années.\
                        Vous pouvez accéder au dashboard via la barre de navigation ou en cliquant directement ci-dessous.",


                                style={"color": "#000406"},

                            ),
                            dbc.Row(
                                [
                                    #Navlink dashbord
                                    dbc.NavLink("Accès Dashbsoard", href="/dashboard",style={'color':'blue'})
                                ])
                        ]

                         )

                ,style={'color':'red','backgroundColor':'white'})
                    ], justify="center", align="center"
                    ),
     html.Br(),
     dbc.Row([dbc.Col(date_picker, lg=4),dbc.Col(table, lg=8)]),
],style={"height": "100vh"}
)

tab1_layout =  html.Div([body],style={'background-image': 'url("/assets/bg.jpg")'})
