# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 16:17:47 2022

@author: Juliette
"""
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
#from dash.dependencies import Input, Output



# Chargement des données
df = pd.read_excel('input.xlsx')

# liste stockant les noms des entreprises
liste_entreprises = df['Groupe'].sort_values()
#print (liste)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(id = "entreprises",
    options=[{'label': i, 'value': i} for i in liste_entreprises],
    multi=False,
    searchable=True,
    placeholder='Select a company')
])

# code à ajouter pour prendre en compte le filtre "entreprise" sur les graphes et tableaux
#@app.callback(
#    Output('output', 'children'), 
#    Input('entreprises', 'value'))
#def update_figure(value):
#    return ...

if __name__ == '__main__':
    app.run_server(debug=True)
    

