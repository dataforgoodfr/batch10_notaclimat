# Libraries import

from dash import html
from utils import card_style, t1b7_df
import flag
import ast

# Bloc title


def infos(selected_company):
    top_brands = ast.literal_eval(t1b7_df[t1b7_df['company_name'] == selected_company]['top_brands'].values[0])

    return html.Div(
        children=[
            html.Div([
                html.Div([
                    html.Img(src=t1b7_df[t1b7_df['company_name'] == selected_company]['brand_logo'].values[0],
                             className="w-100 img-thumbnail"),
                ],
                         className="col",
                         style={"maxWidth": "110px"}),
                html.Div([
                    html.Div(selected_company + " " +
                             flag.flag(t1b7_df[t1b7_df['company_name'] == selected_company]['country_flag'].values[0]),
                             className="h3"),
                    #html.Div('Sector: ' + t1b7_df[t1b7_df['company_name'] == selected_company]['sector'].values[0], #English version
                    html.Div('Secteur : ' + t1b7_df[t1b7_df['company_name'] == selected_company]['sector'].values[0], #French version
                             className="text-muted text-nowrap"),
                    html.Div([
                        #'Revenue: ' + t1b7_df[t1b7_df['company_name'] == selected_company]['revenue'].values[0].round( #English version
                        'C.A : ' + t1b7_df[t1b7_df['company_name'] == selected_company]['revenue'].values[0].round( #French version
                            decimals=1).astype(str) + ' B (' +
                        t1b7_df[t1b7_df['company_name'] == selected_company]['revenue_year'].values[0].astype(str) + ')'
                    ],
                             className="text-muted text-nowrap")
                ],
                         className="col"),
            ],
                     className="row"),
            #html.Div('Main brands:', className="h5 mt-3"), #English version
            html.Div('Principales marques :', className="h5 mt-3"), #French version
            #dash_table.DataTable({'test' : t1b7_df[t1b7_df['company_name']==selected_company]['top_brands'].values[0]})
            #html.Code(tabulate(t1b7_df[t1b7_df['company_name']==selected_company]['top_brands'].values[0], tablefmt='html'))
            html.Ul(
                [html.Li(i, className="list-group-item") for i in top_brands],
                className="list-group p-0",
            )
        ],
        className=card_style)
