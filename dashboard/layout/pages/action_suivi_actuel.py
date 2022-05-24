from dash import html, dcc
from utils import card_style
import dash_daq as daq
from utils import t1b2_df
import plotly.graph_objects as go
import numpy as np

#printable_columns = ['company_name', 'global_score_logo_path', 'direct_score_short_label', 'complete_score_short_label', 'direct_score_hexa_color_code', 'complete_score_hexa_color_code']

def get_filtered_data(df, selected_company):
    df_filtered = df[df['company_name'] == selected_company].reset_index(drop=True)
    return df_filtered


def get_data(df, column_name):
    '''
    Extracts info from a dataframe. Used to improve code lisibility.
    '''
    value = df.loc[0, column_name]
    return value


def top_left(selected_company):
    df = get_filtered_data(t1b2_df, selected_company)
    value = get_data(df, 'direct_score_short_label')
    color = get_data(df, 'direct_score_hexa_color_code')
    pic = 'assets/Picto_usine.png'
    return value, color, pic

def generate_topleft_item(selected_company):
    value_topleft, color_topleft, pic_topleft = top_left(selected_company)
    return html.Div([
        html.Table(
            [
                html.Tbody([
                    html.Tr([
                        html.Td(html.Img(src=pic_topleft),
                                rowSpan=2,
                                className="me-1"),
                        html.Td('Réduction de ses propres émissions', className="fw-bold"),
                    ]),
                    html.Tr([
                        daq.Indicator(color=color_topleft,
                            value=True
                        ),
                        html.Td('\u279c ' + value_topleft,
                                className="px-2"),
                    ],
                            className="align-baseline")
                ])
            ],
            className="align-middle table table-borderless text-center mb-0"
        )
    ])


def top_right(selected_company):
    df = get_filtered_data(t1b2_df, selected_company)
    value = get_data(df, 'complete_score_short_label')
    color = get_data(df, 'complete_score_hexa_color_code')
    pic = 'assets/frames/Picto_lifecycle.png'
    return value, color, pic


def generate_topright_item(selected_company):
    value_topright, color_topright, pic_topright = top_right(selected_company)
    return html.Div([
        html.Table(
            [
                html.Tbody([
                    html.Tr([
                        html.Td(html.Img(src=pic_topright),
                                rowSpan=2,
                                className="me-1"),
                        html.Td('Réduction de son empreinte carbone', className="fw-bold"),
                    ]),
                    html.Tr([
                        daq.Indicator(color=color_topright,
                            value=True
                        ),
                        html.Td('\u279c ' + value_topright,
                                className="px-2"),
                    ],
                            className="align-baseline")
                ])
            ],
            className="align-middle table table-borderless text-center mb-0"
        )
    ])
    
  
def bottom_left(selected_company):
    df = get_filtered_data(t1b2_df, selected_company)
    values = []
    col_list = ['c1_final_value', 
    'c1_2_deg_final', 
    'c1_1_8_deg_final',
    'c1_1_5_deg_final'
    ]
    
    for col in col_list:
        val = get_data(df, col)
        if val != np.nan:
            values.append(val-1)
        else: values.append(0)
    
    colors = [get_data(df, 'direct_score_hexa_color_code'), '#FEC800', '#8CDF41', '#0DB800']
    
    return values, colors


def generate_bottomleft_item(selected_company):
    scenarios=[selected_company, '1.5°C scenario', '1.8°C scenario', '2°C scenario']
    values, colors = bottom_left(selected_company)
   
    fig = go.Figure([go.Bar(x=scenarios, y=values, text=values, marker_color=colors)])
    fig.update_traces(texttemplate='%{text:.1%}', textposition='inside')
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title="Réduction dees émissions de GES", tickformat=".0%")
    
    return html.Div([
        dcc.Graph(figure=fig)
    ])

def bottom_right(selected_company):
    df = get_filtered_data(t1b2_df, selected_company)
    values = []
    col_list = ['c2_final_value', 
    'c2_2_deg_final', 
    'c2_1_8_deg_final',
    'c2_1_5_deg_final'
    ]
    
    for col in col_list:
        val = get_data(df, col)
        if val != np.nan:
            values.append(val-1)
        else: values.append(0)
    
    colors = [get_data(df, 'direct_score_hexa_color_code'), '#FEC800', '#8CDF41', '#0DB800']
    
    return values, colors


def generate_bottomright_item(selected_company):
    scenarios=[selected_company, '1.5°C scenario', '1.8°C scenario', '2°C scenario']
    values, colors = bottom_right(selected_company)
   
    fig = go.Figure([go.Bar(x=scenarios, y=values, text=values, marker_color=colors)])
    fig.update_traces(texttemplate='%{text:.1%}', textposition='inside')
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title="Réduction de l'empreinte carbone", tickformat=".0%")
    
    return html.Div([
        dcc.Graph(figure=fig)
    ])


def action_suivi_actuel(selected_company):
    return html.Div(
        children=[
            html.Div("Action actuelle - Suivi des engagements", className="h5"),
            html.Div(
                children=[
                    html.Div(
                        children=[
                        generate_topleft_item(selected_company),
                        generate_topright_item(selected_company)
                    ]),
                    html.Div(
                        children=[
                        generate_bottomleft_item(selected_company),
                        generate_bottomright_item(selected_company)
                    ])
                ]
            )
        ]
    )
    
    