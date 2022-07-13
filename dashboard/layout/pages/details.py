# from turtle import back
# import pandas as pd
from dash import dcc, html
from utils import dataviz_df
import plotly.express as px


def get_company_details(df, selected_company):
    
    df = df[df['company_name'] == selected_company]

    # Make lists from amount, name and hover
    amount = [float(i) for i in df['emissions_category_amount'].iloc[0].split(',')]
    name = df['emissions_category_name'].iloc[0].split(',')
    hover = df['emissions_category_hover'].iloc[0].split(',')

    return df, amount, name, hover


# Generate bar chart
def details(selected_company):
    df, amount, name, hover = get_company_details(dataviz_df, selected_company)
    fig = px.bar(
        data_frame = df,
        x=[1, 1, 1, 1, 1, 1],
        y=amount,
        color=name,
        hover_name=hover,
        text=amount,
        labels={'y':'Emissions'},
        color_discrete_sequence= px.colors.sequential.Plotly3
        )

    fig.update_layout({
        'plot_bgcolor': 'rgba(255, 255, 255, 255)',
        'paper_bgcolor': 'rgba(255, 255, 255, 255)',
        },
        legend_title="Catégories",
        uniformtext_minsize=6,
        )

    fig.data = fig.data[::-1]
    fig.layout.legend.traceorder = 'reversed'

    fig.update_traces(textposition='inside',
                      texttemplate='%{text:.1%}',
                      hovertemplate='<b>Information</b>: %{hovertext}'
    # + "<br><b>Emissions</b>: %{y}%<br><extra></extra>"
    )
    
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_yaxes(visible=False, showticklabels=False)


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
