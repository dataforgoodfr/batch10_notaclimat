from dash import html, dcc

import dash_bootstrap_components as dbc
import dash_daq as daq

from utils import card_style
from utils import t1b2_df

import plotly.graph_objects as go
import plotly.figure_factory as ff

import numpy as np

# Colorbars for bullet gauge
color_bars = ['#820000', '#C00000', '#FF8939', '#FEC800', '#8CDF41', '#0DB800']


def get_filtered_data(df, selected_company):
    df_filtered = df[df['company_name'] == selected_company].reset_index(drop=True)
    return df_filtered


def get_data(df, column_name):
    '''
    Extracts info from a dataframe. Used to improve code lisibility.
    '''
    value = df.loc[0, column_name]
    return value


def build_bullet_gauge(engagement, accomplishment, color_accomplishment):
    '''
    Builds the custom Bullet Gauge for the dashboard.
    Takes 2 values for the engagement & accomplishment from the selected_company
    Returns the gauge with colors varying from green to dark red, with cursors on both sides representing:
    - in white, on the right side: the engagement from the company, expressed as a score
    - in color, on the left side: the actual accomplishments from the same company, expressed as a score
    '''

    # Building custom bullet gauge
    data = [{"ranges": [1, 7, 6], "measures": [x for x in range(1, 7)]}]
    width = 0.5

    traces = []
    fig = go.Figure()

    for i in range(0, 6):
        trace = go.Bar(x=[0], y=[1], orientation='v', width=width, marker_color=color_bars[i], showlegend=False)
        traces.insert(0, trace)

    fig.add_traces(traces)
    fig.update_layout(barmode='stack')

    # Building left cursor: accomplishment
    trace1 = go.Scatter(x=[-0.1 - width],
                        y=[7 - accomplishment],
                        marker={
                            'symbol': 'arrow-right',
                            'color': color_accomplishment,
                            'size': 25,
                        },
                        name='Accomplishment',
                        xaxis='x1',
                        yaxis='y1',
                        hovertemplate='Accomplissement',
                        showlegend=False)

    # Building right cursor: engagement
    trace2 = go.Scatter(x=[0.1 + width],
                        y=[7 - engagement],
                        marker={
                            'symbol': 'arrow-left',
                            'color': 'white',
                            'line': {
                                'color': 'black',
                                'width': 1
                            },
                            'size': 20
                        },
                        name='Engagement',
                        xaxis='x1',
                        yaxis='y1',
                        hovertemplate='Engagement',
                        showlegend=False)

    # Fixing ticks
    fig.update_xaxes(ticks="outside", nticks=3)
    fig.update_yaxes(layer="below traces",
                     tickmode='array',
                     tickvals=[1, 2, 3, 4, 5, 6],
                     ticktext=['+1.5°', '', '+2°C', '', '+4°C', ''])

    # Deleting the background
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # Adding cursors
    fig.add_traces([trace1, trace2])

    return fig


def top_left(selected_company):
    df = get_filtered_data(t1b2_df, selected_company)
    value = get_data(df, 'direct_score_short_label')
    color = get_data(df, 'direct_score_hexa_color_code')
    pic = 'assets/frames/Picto_usine.png'
    return value, color, pic


def generate_topleft_item(selected_company):
    value_topleft, color_topleft, pic_topleft = top_left(selected_company)
    return html.Div([
        html.Table([
            html.Tbody([
                html.Tr([
                    html.Td(html.Img(src=pic_topleft), rowSpan=2, className="me-1"),
                    html.Td('Réduction de ses propres émissions', className="fw-bold"),
                ]),
                html.Tr([
                    daq.Indicator(color=color_topleft, value=True),
                    html.Td('\u279c ' + value_topleft, className="px-2"),
                ],
                        className="align-baseline")
            ])
        ],
                   className="align-middle table table-borderless text-center mb-0")
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
        html.Table([
            html.Tbody([
                html.Tr([
                    html.Td(html.Img(src=pic_topright), rowSpan=2, className="me-1"),
                    html.Td('Réduction de son empreinte carbone', className="fw-bold"),
                ]),
                html.Tr([
                    daq.Indicator(color=color_topright, value=True),
                    html.Td('\u279c ' + value_topright, className="px-2, text-center"),
                ],
                        className="align-baseline")
            ])
        ],
                   className="align-middle table table-borderless mb-0")
    ])


def bottom_left(selected_company):
    df = get_filtered_data(t1b2_df, selected_company)
    values = []
    col_list = ['c1_final_value', 'c1_2_deg_final', 'c1_1_8_deg_final', 'c1_1_5_deg_final']

    for col in col_list:
        val = get_data(df, col)
        if val != np.nan:
            values.append(val - 1)
        else:
            values.append(0)

    engagement = get_data(df, 'direct_score_commitments')
    accomplishment = get_data(df, 'direct_score')
    color_accomplishment = get_data(df, 'direct_score_hexa_color_code')
    colors = [color_accomplishment, '#FEC800', '#8CDF41', '#0DB800']

    return values, colors, engagement, accomplishment, color_accomplishment


def generate_bottomleft_item(selected_company):
    scenarios = [selected_company, '2°C scenario', '1.8°C scenario', '1.5°C scenario']
    values, colors, engagement, accomplishment, color_accomplishment = bottom_left(selected_company)

    fig = go.Figure([go.Bar(x=scenarios, y=values, text=values, marker_color=colors)])
    fig.update_traces(texttemplate='%{text:.1%}', textposition='inside')
    fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(title="Réduction des émissions de GES", tickformat=".0%")
    fig.update_xaxes(tickangle = 90, automargin=True)

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig),
                    style={
                        'width': '60%',
                        'min-width': '60%',
                        'max-width': '60%',
                        #'height': '100%'
                    }),
            dbc.Col(dcc.Graph(figure=build_bullet_gauge(engagement, accomplishment, color_accomplishment)),
                    style={
                        'width': '40%',
                        'min-width': '40%',
                        'max-width': '40%',
                        #'height': '100%'
                    },
                    className="p-0"
                    )
        ])
    ],
                    className="d-flex flex-column border"
                    )


def bottom_right(selected_company):
    df = get_filtered_data(t1b2_df, selected_company)
    values = []
    col_list = ['c2_final_value', 'c2_2_deg_final', 'c2_1_8_deg_final', 'c2_1_5_deg_final']

    for col in col_list:
        val = get_data(df, col)
        if val != np.nan:
            values.append(val - 1)
        else:
            values.append(0)

    engagement = get_data(df, 'complete_score_commitments')
    accomplishment = get_data(df, 'complete_score')
    color_accomplishment = get_data(df, 'complete_score_hexa_color_code')
    colors = [color_accomplishment, '#FEC800', '#8CDF41', '#0DB800']

    return values, colors, engagement, accomplishment, color_accomplishment


def generate_bottomright_item(selected_company):
    scenarios = [selected_company, '2°C scenario', '1.8°C scenario', '1.5°C scenario']
    values, colors, engagement, accomplishment, color_accomplishment = bottom_right(selected_company)

    fig = go.Figure([go.Bar(x=scenarios, y=values, text=values, marker_color=colors)])
    fig.update_traces(texttemplate='%{text:.1%}', textposition='inside')
    fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(title="Réduction de l'empreinte carbone", tickformat=".0%",)
    fig.update_xaxes(tickangle = 90, automargin=True)

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig),
                    style={
                        'width': '60%',
                        #'min-width': '60%',
                        #'max-width': '60%',
                        #'height': '100%'
                    }),
            dbc.Col(dcc.Graph(figure=build_bullet_gauge(engagement, accomplishment, color_accomplishment)),
                    style={
                        'width': '40%',
                        #'min-width': '40%',
                        #'max-width': '40%',
                        #'height': '100%'
                    },
                    className="p-0")
        ])
    ],
                    className="d-flex flex-column border")


def action_suivi_actuel(selected_company):
    return dbc.Container([
        html.Div("Action actuelle - Suivi des engagements", className="h5"),
        html.Div(
            dbc.Row([
                dbc.Col(generate_topleft_item(selected_company), className='d-inline p-2', style={'width': '49%'}),
                dbc.Col(generate_topright_item(selected_company), className='d-inline p-2', style={'width': '49%'}),
            ],
                    style={
                        'width': '80%',
                        'vertical-align': 'middle'
                    })),
        html.Div(
            dbc.Row([
                dbc.Col(generate_bottomleft_item(selected_company), className='d-inline p-2', style={'width': '49%'}),
                dbc.Col(generate_bottomright_item(selected_company), className='d-inline p-2', style={'width': '49%'}),
            ],
                    style={'vertical-align': 'middle'}))
    ]
    ,                         className="d-flex flex-column")
