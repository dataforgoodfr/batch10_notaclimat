import pandas as pd
from dash import dcc, html
from utils import t1b6_df


def get_company_details(df, selected_company):
    global amount, name, hover

    df = df[df['company_name'] == selected_company]

    # Make lists from amount, name and hover
    amount = list(df['emissions_category_amount'].iloc[0].split(','))
    name = list(df['emissions_category_name'].iloc[0].split(','))
    hover = list(df['emissions_category_hover'].iloc[0].split(','))

    return df


# Generate pie chart
def details(selected_company):
    df = get_company_details(t1b6_df, selected_company)

    return html.Div(children=[
        html.Div("Détail des émissions", className="h5 p-3"),
        html.Div([
            dcc.Graph(id="details",
                      figure={
                          "data": [{
                              "values": amount,
                              "labels": name,
                              "hole": .4,
                              "type": "pie"
                          }],
                          "layout": {
                              "paper_bgcolor": "#ffffff",
                              "annotations": [{
                                  "font": {
                                      "size": 12
                                  },
                                  "showarrow": False,
                                  "text": "",
                                  "x": 0.5,
                                  "y": 0.5
                              }],
                              "showlegend": False
                          }
                      })
        ],
                 className="m-0 p-0")
    ],
                    className="row card rounded p-0")
