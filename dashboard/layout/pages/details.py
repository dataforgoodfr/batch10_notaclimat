from turtle import back
import pandas as pd
from dash import dcc, html
from utils import t1b6_df
import plotly.express as px
import plotly.graph_objs as go


def get_company_details(df, selected_company):
    global amount, name, hover, x

    df = df[df['company_name'] == selected_company]

    # Make lists from amount, name and hover
    amount = [int(i) for i in df['emissions_category_amount'].iloc[0].split(',')]
    name = df['emissions_category_name'].iloc[0].split(',')
    hover = df['emissions_category_hover'].iloc[0].split(',')

    return df


# Generate bar chart
def details(selected_company):
    df = get_company_details(t1b6_df, selected_company)
    fig = px.bar(
        x=[1, 1, 1, 1, 1, 1],
        y=amount,
        color=name,
        hover_name=hover,
        labels={'y':'% Emissions'}
        )

    fig.update_layout({
        'plot_bgcolor': 'rgba(255, 255, 255, 255)',
        'paper_bgcolor': 'rgba(255, 255, 255, 255)',
        },
        legend_title="Catégories"
        )

    fig.data = fig.data[::-1]
    fig.layout.legend.traceorder = 'reversed'

    fig.update_traces(hovertemplate='<b>Information</b>: %{hovertext}' +
    "<br><b>Emissions</b>: %{y}%<br><extra></extra>")
    
    fig.update_xaxes(visible=False, showticklabels=False)


    return html.Div(children=[
        html.Div("Détail des émissions", className="h5 p-3"),
        html.Div([  
            dcc.Graph(id="details",
                      figure=fig,
                      style={'backgroundColor': '#000000'},
                      config= {'displayModeBar': False}
                    )
        ],
                 className="m-0 p-0")
    ],
                    className="row card rounded p-0")
