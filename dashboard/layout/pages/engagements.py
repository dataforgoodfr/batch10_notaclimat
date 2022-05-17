from dash import html
import dash_daq as daq
from utils import card_style, t1b5_df


def engagements(selected_company):
    return html.Div(children=[
        html.Div('Ses engagements', className="h5"),
        html.Div(t1b5_df[t1b5_df['company_name'] == selected_company]['direct_commitments_sentence'],
                 className="fst-italic"),
        html.Div([
            daq.Indicator(color=t1b5_df[t1b5_df['company_name'] == selected_company]['direct_ambition_hexa_color_code'],
                          value=True),
            html.Div(t1b5_df[t1b5_df['company_name'] == selected_company]['direct_ambition_long_label'],
                     className="text-muted"),
        ],
                 className="d-flex align-items-center gap-2 mt-2 mb-3"),
        html.Div(t1b5_df[t1b5_df['company_name'] == selected_company]['complete_commitments_sentence'],
                 className="fst-italic"),
        html.Div([
            daq.Indicator(
                color=t1b5_df[t1b5_df['company_name'] == selected_company]['complete_ambition_hexa_color_code'],
                value=True),
            html.Div(t1b5_df[t1b5_df['company_name'] == selected_company]['complete_ambition_long_label'],
                     className="text-muted"),
        ],
                 className="d-flex align-items-center gap-2 mt-2"),
    ],
                    className=card_style)
