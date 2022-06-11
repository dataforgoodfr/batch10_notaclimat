from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from utils import t2b2_df, card_style


def get_filtered_data(df, selected_companies):
    df_filtered = df[df['company_name'].isin(selected_companies)].reset_index(drop=True)
    return df_filtered


def get_data(df, column_name):
    '''
    Extracts info from a dataframe. Used to improve code lisibility.
    '''
    values = df.loc[:, column_name]
    return values


def build_lollipop_chart(accomplishment, color_accomplishment, companies_names, df):

    fig = go.Figure()

    #Create scatter trace
    fig.add_trace(
        go.Scatter(
            y=7 - accomplishment,
            x=companies_names,
            mode='markers',
            marker_color=color_accomplishment,
            marker_size=20,
        ))

    #Set axes ranges
    fig.update_xaxes(
        ticks="outside",
        tickangle=45,
        tickfont_size=15,
    )
    fig.update_yaxes(layer="below traces",
                     tickmode='array',
                     tickvals=[1, 2, 3, 4, 5, 6, 7],
                     ticktext=['+1.5°C', '+1.8°C', '+2°C', '+3°C', '+4°C', '', ''])

    #Add shapes
    for i in range(len(df)):
        fig.add_shape(type='line', x0=i, y0=4, x1=i, y1=(7 - accomplishment[i]), line=dict(
            color='grey',
            width=1,
        ))
    fig.add_shape(type='line', x0=0, y0=4, x1=len(df) - 1, y1=4, line=dict(
        color='grey',
        width=3,
    ))
    fig.update_shapes(dict(xref='x', yref='y'))

    #Set figure size and delete the background
    fig.update_layout(width=800, height=600, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig


def chart_left(selected_companies):
    df = get_filtered_data(t2b2_df, selected_companies)
    df = df.sort_values(by='direct_level').reset_index(drop=True)
    accomplishment = get_data(df, 'direct_level')
    color_accomplishment = get_data(df, 'direct_score_hexa_color_code')
    companies_names = get_data(df, 'company_name')

    return accomplishment, color_accomplishment, companies_names, df


def chart_right(selected_companies):
    df = get_filtered_data(t2b2_df, selected_companies)
    df = df.sort_values(by='complete_level').reset_index(drop=True)
    accomplishment = get_data(df, 'complete_level')
    color_accomplishment = get_data(df, 'complete_score_hexa_color_code')
    companies_names = get_data(df, 'company_name')

    return accomplishment, color_accomplishment, companies_names, df


def generate_chart_left(selected_companies):
    accomplishment, color_accomplishment, companies_names, df = chart_left(selected_companies)

    return html.Div(children=[
        html.Div("Concernant leurs propres émissions", className="h5 p-3"),
        html.Div(dcc.Graph(figure=build_lollipop_chart(accomplishment, color_accomplishment, companies_names, df),
                           style={
                               'width': '100%',
                               'minWidth': '100%',
                               'maxWidth': '100%',
                               'height': '100%'
                           }),
                 style={'display': 'inline-block'}),
    ])


def generate_chart_right(selected_companies):
    accomplishment, color_accomplishment, companies_names, df = chart_right(selected_companies)

    return html.Div(children=[
        html.Div("Concernant leur empreinte carbone complète", className="h5 p-3"),
        html.Div(dcc.Graph(figure=build_lollipop_chart(accomplishment, color_accomplishment, companies_names, df),
                           style={
                               'width': '100%',
                               'minWidth': '100%',
                               'maxWidth': '100%',
                               'height': '100%'
                           }),
                 style={'display': 'inline-block'}),
    ])


def reduction_rate(selected_companies):
    return html.Div(children=[
        html.Div(" Niveaux de réduction actuels comparés aux trajectoires climatiques", className="h3 p-0"),
        html.Div(dbc.Row([
            dbc.Col(generate_chart_left(selected_companies), className='d-inline p-2', style={'width': '49%'}),
            dbc.Col(generate_chart_right(selected_companies), className='d-inline p-2', style={'width': '49%'}),
        ],
                         style={
                             'width': '100%',
                             'verticalAlign': 'middle'
                         }),
                 className="flex-shrink-1 overflow-auto"),
        html.Hr(),
        html.Div([", ".join(selected_companies)])
    ],
                    className=card_style + " flex-nowrap h-100 overflow-auto p-3")