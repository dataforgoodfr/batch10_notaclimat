# Libraries import

from dash import html
from utils import card_style, t1b7_df
from tabulate import tabulate

# Bloc title

def infos(selected_company):
    return html.Div(id='root_div', children=[
        html.Div([html.Img(src=t1b7_df[t1b7_df['company_name']==selected_company]['brand_logo'].values[0], height=50)]),
        html.Div(selected_company + t1b7_df[t1b7_df['company_name']==selected_company]['country_flag'].values[0]),
	html.Div('Sector: ' + t1b7_df[t1b7_df['company_name']==selected_company]['sector'].values[0]),
	html.Div('Revenue: $' + t1b7_df[t1b7_df['company_name']==selected_company]['revenue'].values[0].round(decimals=1).astype(str) + ' B (' +t1b7_df[t1b7_df['company_name']==selected_company]['revenue_year'].values[0].astype(str) + ')'),
	html.Div('Top brands:'),
	#dash_table.DataTable({'test' : t1b7_df[t1b7_df['company_name']==selected_company]['top_brands'].values[0]})
	#html.Code(tabulate(t1b7_df[t1b7_df['company_name']==selected_company]['top_brands'].values[0], tablefmt='html'))
	html.Div(t1b7_df[t1b7_df['company_name']==selected_company]['top_brands'].values[0])
	], className=card_style)
