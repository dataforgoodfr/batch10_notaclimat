from dash import html
from utils import card_style, t1b4_df

def get_sector(df, selected_company):
    index = df[df['company_name'] == selected_company].index[0]
    sector = df.loc[index, 'Sector']
    return sector

def get_filtered_data(df, sector):
    df_filtered = df[df['Sector'] == sector]
    return df_filtered

def sector_compare(selected_company):
    sector = get_sector(t1b4_df, selected_company)
    sector_compare_information = get_filtered_data(t1b4_df, sector)
    return html.Div(
        children=[
            html.Div("Comparaison Sectorielle", className="h5"),
            html.Div([
                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td('Entreprises', className="fw-bold"),
                            html.Td('Réduction actuelle', className="fw-bold"),
                            html.Td('Réduction de ses propres émissions', className="fw-bold"),
                            html.Td('Réduction de son empreinte carbone', className="fw-bold")
                        ]),
                        html.Tr([
                            html.Td(sector_compare_information['company_name'][0], className="px-2"),
                            html.Td(html.Img(
                                src=sector_compare_information['global_score_pic'][0]),
                                className="me-1"
                                ),
                            html.Td('\u279c ' + sector_compare_information['c1_label'][0],
                                    className="px-2",
                                    style={'color': sector_compare_information['c1_color'][0]}),
                            html.Td('\u279c ' + sector_compare_information['c2_label'][0],
                                    className="px-2",
                                    style={'color': sector_compare_information['c2_color'][0]})
                        ],className="align-baseline"
                        )
                    ])
                ],className="align-middle table table-borderless text-center mb-0")
            ], className=card_style)
        ]
    )
