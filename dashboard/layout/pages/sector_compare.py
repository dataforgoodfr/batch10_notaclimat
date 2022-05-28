from dash import html
from utils import t1b4_df, card_style

df_t1b4 = t1b4_df

printable_columns = [
    'company_name', 'global_score_logo_path', 'direct_score_short_label', 'complete_score_short_label',
    'direct_score_hexa_color_code', 'complete_score_hexa_color_code'
]


def get_sector(df, selected_company):
    '''
    Extracts sector for selected_company
    '''
    index = df[df['company_name'] == selected_company].index[0]
    sector = df.loc[index, 'sector']
    return sector


def get_filtered_data(df, selected_company):
    df_filtered = df[df['sector'] == get_sector(df, selected_company)].reset_index(drop=True)
    return df_filtered


def generate_html_table(df, max_rows, selected_company):
    rows = []
    for i in range(0, max_rows):
        image_filename = df.iloc[i]['global_score_logo_path']
        rows.append(
            html.Tr([
                html.Td(df.iloc[i]['company_name'], className="fw-bold"),
                html.Td(html.Img(src=image_filename), className="me-1"),
                html.Td('\u279c ' + df.iloc[i]['direct_score_short_label'],
                        className="px-2",
                        style={'color': df['direct_score_hexa_color_code'][i]}),
                html.Td('\u279c ' + df.iloc[i]['complete_score_short_label'],
                        className="px-2",
                        style={'color': df['complete_score_hexa_color_code'][i]})
            ],
                    id=str(i),
                    className="align-baseline"))

    return html.Div(children=[
        html.Div("Comparaison sectorielle - " + selected_company, className="h4 mb-3"),
        html.Div([
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Td('Entreprises', className="fw-bold py-3 sticky-top align-middle"),
                        html.Td('Réduction actuelle', className="fw-bold py-3 sticky-top align-middle"),
                        html.Td('Réduction de ses propres émissions', className="fw-bold py-3 sticky-top align-middle"),
                        html.Td('Réduction de son empreinte carbone', className="fw-bold py-3 sticky-top align-middle")
                    ],
                            className="table-primary p-2 sticky-top")
                ],
                           className="sticky-top"),
                html.Tbody(rows)
            ],
                       className="align-middle table table-borderless table-bordered text-center mb-1")
        ],
                 className="flex-shrink-1 overflow-auto")
    ],
                    className=card_style + " flex-nowrap h-100 overflow-auto p-3")


def sector_compare(selected_company):
    sector_compare_information = get_filtered_data(df_t1b4, selected_company)[printable_columns]
    return generate_html_table(sector_compare_information, len(sector_compare_information), selected_company)
