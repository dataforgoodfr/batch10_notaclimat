# Code to explicit

from datetime import datetime as dt
from datetime import date, timedelta
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
#Import des données
df_pc=pd.read_csv('data/data_pc.csv')
df_pc['dates'] = pd.to_datetime(df_pc['dates'],format='%Y-%m-%d')
#fonction de mise à  jour de la table
def update_first_datatable(start_date,end_date,type):
    if start_date is not None:
            start_date= dt.strptime(start_date, '%Y-%m-%d')
            start_date_string = start_date.strftime('%Y-%m-%d')
    if end_date is not None:
            end_date =dt.strptime(end_date, '%Y-%m-%d')
            end_date_string = end_date.strftime('%Y-%m-%d')
    if type=='defaut':
        data_df=df_pc[(df_pc['dates']>=start_date_string) & (df_pc['dates']<=end_date_string)]
    data_df['dates']=data_df['dates'].dt.date
    return data_df.to_dict("rows")


######################## Fonction de mise à jour du graph (line et bar)  ########################

def update_graph(start_date, end_date,type):
    if start_date is not None:
            start_date= dt.strptime(start_date, '%Y-%m-%d')
            start_date_string = start_date.strftime('%Y-%m-%d')
    if end_date is not None:
            end_date =dt.strptime(end_date, '%Y-%m-%d')
            end_date_string = end_date.strftime('%Y-%m-%d')

    if type=='trafic':
        data_df=df_pc[(df_pc['dates']>=start_date_string) & (df_pc['dates']<=end_date_string)]

    dict_graph={}
    for value in data_df.columns.to_list()[1:]:
        if '%' not in value:

            dict_graph[value]= go.Scatter(
	      x=data_df.dates,
	      y=data_df[value],
	      text=value,
	      name=value

            )


    fig = make_subplots(
      rows=1,
      cols=2,
      shared_xaxes=True,
      column_widths=[0.7, 0.3],
      subplot_titles=(								# Être sûr d'avoir le même nombre de titre que de ligne
        'Trafic détaillé par Appareil','Trafic résumé par type '
        ))

    for key, value in dict_graph.items():
        fig.add_traces(value, 1, 1)

    #################s######format data bar
    data_df['Phone']=data_df['android']+data_df['iphone_ipad']
    data_df['Pc']= data_df['autre_pc']+data_df['mac']
    data_df=data_df[['Phone','Pc']]
    labels=data_df.sum(axis=0).index.tolist()
    values= data_df.sum(axis=0).tolist()

    Bar=go.Bar(
        x=labels,
        y=values,
        marker={"color":[ "#97151c",'#D9CB04']},
        name="Device Use",
    )


    fig.add_trace(Bar, 1, 2)

#####################

    fig['layout'].update(

     paper_bgcolor = '#000406',
     font_color = "white"
      )
    updated_fig = fig


    return updated_fig


###################Fin mise à jour graphique(line et bar)@###################

######################## Fonction de mise à jour du graph pie  ########################
def update_pie(start_date, end_date,type):
    if start_date is not None:
            start_date= dt.strptime(start_date, '%Y-%m-%d')
            start_date_string = start_date.strftime('%Y-%m-%d')
    if end_date is not None:
            end_date =dt.strptime(end_date, '%Y-%m-%d')
            end_date_string = end_date.strftime('%Y-%m-%d')

    if type=='trafic':

        data_df=df_pc[(df_pc['dates']>=start_date_string) & (df_pc['dates']<=end_date_string)]

    data_df['Ios'] = data_df['iphone_ipad']+df_pc['mac']
    data_df=data_df[['Ios','android','autre_pc']]
    data_df.columns=['Ios','Android','Autre_Os']
    labels=data_df.sum(axis=0).index.tolist()
    values= data_df.sum(axis=0).tolist()

    fig = go.Figure(data=[go.Pie(labels=labels, values=values,hole=.7)])
    #

    fig.update_traces(
    name= "Os",
    marker=dict(colors=['gold', 'mediumturquoise'], line=dict(color='#000000', width=2)),
    hoverinfo ='label+name+percent',
    #textinfo='value'
    )

    fig['layout'].update(

    paper_bgcolor="#111111",
    font_color = "white",
    annotations=[{"font": {"size": 20},
    "text": "Accès par Os","y": 0.4}]
    #showlegend= Fals
    )
    final_fig=fig
    return final_fig
