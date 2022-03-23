import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html
from dash import dcc


data = pd.read_csv(r'US_Accidents_Dec20_new.csv', nrows=10000)
data1=data[['ID','Temperature(F)','Wind_Chill(F)','Humidity(%)','Visibility(mi)','Wind_Direction','Wind_Speed(mph)','Precipitation(in)','Civil_Twilight','Nautical_Twilight','Astronomical_Twilight','Weather_Condition']]
data2=data[['City','County','State','Timezone','Start_Lat','Start_Lng','End_Lat','End_Lng']]
data_merged = pd.concat([data1, data2], axis=1)


data1.fillna(data1.median(), inplace=True)
data2.fillna(data1.median(), inplace=True)
data_merged.fillna(data1.median(), inplace=True)

fig33 = px.bar(data_merged, x='Humidity(%)', y='Visibility(mi)', color='Precipitation(in)',  
   barmode='group')


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Weather Conditions'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Visualising trends across different weather conditions impacting accidents'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Humidity vs Visibility',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dcc.Graph(figure=fig33),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Humidity vs Temperature',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Humidity(%)"],
                        "y": data["Temperature(F)"],
                        "type": "scatter",
                        'mode':'markers',
                        'color':data['City']
                    },
                ],
                "layout": {
                    "xaxis": {"title":"Humidity (%)"},
                    "yaxis": {"title":"Temperature (F)"}
                },
            },
        ),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Windchill vs Temperature',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Wind_Chill(F)"],
                        "y": data["Temperature(F)"],
                        "type": "scatter",
                        'mode':'markers',
                        'color':data['City']
                    },
                ],
                "layout": {
                    "xaxis": {"title":"Windchill (F)"},
                    "yaxis": {"title":"Temperature (F)"}
                },
            },
        )
        
    ])
        
])
    
# app.run_server(debug=True)
