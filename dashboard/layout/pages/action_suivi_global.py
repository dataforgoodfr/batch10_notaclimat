
from dash import html
from utils import card_style, t1b3_df


def get_company_global_information(df_companies_global_information, selected_company):
    df_company = df_companies_global_information[df_companies_global_information['company_name'] == selected_company]
    df_company = df_company.reset_index(drop=True)

    company_global_information = {}
    company_global_information['company_name'] = df_company['company_name'][0]
    company_global_information['global_score_short_label'] = df_company['global_score_short_label'][0]
    company_global_information['global_score_hexa_color_code'] = df_company['global_score_hexa_color_code'][0]
    company_global_information['direct_score_short_label'] = df_company['direct_score_short_label'][0]
    company_global_information['direct_score_hexa_color_code'] = df_company['direct_score_hexa_color_code'][0]
    company_global_information['complete_score_short_label'] = df_company['complete_score_short_label'][0]
    company_global_information['complete_score_hexa_color_code'] = df_company['complete_score_hexa_color_code'][0]
    company_global_information['global_score_logo_path'] = df_company['global_score_logo_path'][0]
    company_global_information['comment'] = df_company['comment'][0]

    return company_global_information


def action_suivi_global(selected_company):
    company_global_information = get_company_global_information(t1b3_df, selected_company)
    return html.Div(
        children=[
            html.Div([
                html.Div("AU GLOBAL", className="h6 fw-bold"),
                html.Div([
                    html.Table(
                        [
                            # html.Thead([
                            html.Tbody([
                                html.Tr([
                                    html.Td(html.Img(src=company_global_information['global_score_logo_path']),
                                            rowSpan=2,
                                            className="me-1"),
                                    html.Td('Réduction actuelle', className="fw-bold"),
                                    html.Td('Réduction de ses propres émissions', className="fw-bold"),
                                    html.Td('Réduction de son empreinte carbone', className="fw-bold"),
                                    html.Td('Commentaire Nota Climat', className="fw-bold")
                                ]),
                                # ]),
                                html.Tr([
                                    html.Td(company_global_information['global_score_short_label'], className="px-2", 
                                        style={'color': company_global_information['global_score_hexa_color_code']}),
                                    html.Td('\u279c ' + company_global_information['direct_score_short_label'],
                                            className="px-2", 
                                            style={'color': company_global_information['direct_score_hexa_color_code']}),
                                    html.Td('\u279c ' + company_global_information['complete_score_short_label'],
                                            className="px-2",
                                            style={'color': company_global_information['complete_score_hexa_color_code']}),
                                    html.Td(company_global_information['comment'])
                                ],
                                        className="align-baseline")
                            ])
                        ],
                        className="align-middle table table-borderless text-center mb-0")
                ])
            ])
        ],
        className=card_style)

