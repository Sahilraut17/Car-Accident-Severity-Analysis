import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash import html
from dash import dcc
from app import app
from dash.dependencies import Input, Output



data = pd.read_csv(r'US_Accidents_2021_new.csv', nrows=10000)


def generate_intervals_labels(attribute, split, gap):
    var_min = min(data[attribute])
    bins = [int(var_min)]
    labels = []

    for i in range(1, split+1):
        lower_limit = int(var_min+((i-1)*gap))
        if i==split:
            upper_limit = int(max(data[attribute]))
        else:
            upper_limit = int(var_min + (i*gap))
        # bins
        bins.append(upper_limit)
        # labels
        label_var = '({} to {})'.format(lower_limit, upper_limit)
        labels.append(label_var)    
    
    return bins, labels


##### Weather Conditions ########
weather_condition_df = pd.DataFrame(data.Weather_Condition.value_counts().head(10)).reset_index().rename(columns={'index':'Weather Condition', 'Weather_Condition':'Cases'})
weather_condition = px.bar(weather_condition_df, x='Cases', y='Weather Condition', orientation='h', color='Cases', color_continuous_scale='RdBu_r')
weather_condition.update_layout(yaxis={'categoryorder':'total ascending'})

##### Temperature ######
bins_temp, labels_temp = generate_intervals_labels('Temperature(F)', 5, 30)
data["temp_binned"] = pd.cut(data["Temperature(F)"], bins_temp, labels=labels_temp)
df_temp = data.groupby("temp_binned").count().reset_index()
df_temp = df_temp.rename(columns={"ID":"Accident Cases", "temp_binned":"Temperature (F)"})
bar_temp = px.bar(df_temp, x='Temperature (F)', y='Accident Cases')
pie_temp = px.pie(df_temp, values='Accident Cases', names='Temperature (F)', color_discrete_sequence=px.colors.sequential.RdBu,hole=0.5)

##### Humidity ######
bins_humi, labels_humi = generate_intervals_labels('Humidity(%)', 10, 10)
data["humi_binned"] = pd.cut(data["Humidity(%)"], bins_humi, labels=labels_humi)
df_humi = data.groupby("humi_binned").count().reset_index()
df_humi = df_humi.rename(columns={"ID":"Accident Cases", "humi_binned":"Humidity (%)"})
bar_humi = px.bar(df_humi, x='Humidity (%)', y='Accident Cases')
pie_humi = px.pie(df_humi, values='Accident Cases', names='Humidity (%)', color_discrete_sequence=px.colors.sequential.RdBu,hole=0.5)

##### Pressure ######
bins_press, labels_press = generate_intervals_labels('Pressure(in)', 5, 2)
data["press_binned"] = pd.cut(data["Pressure(in)"], bins_press, labels=labels_press)
df_press = data.groupby("press_binned").count().reset_index()
df_press = df_press.rename(columns={"ID":"Accident Cases", "press_binned":"Pressure (in)"})
bar_press = px.bar(df_press, x='Pressure (in)', y='Accident Cases')
pie_press = px.pie(df_press, values='Accident Cases', names='Pressure (in)', color_discrete_sequence=px.colors.sequential.RdBu,hole=0.5)

##### Wind Chill ######
bins_wc, labels_wc = generate_intervals_labels('Wind_Chill(F)', 8, 20)
data["wc_binned"] = pd.cut(data["Wind_Chill(F)"], bins_wc, labels=labels_wc)
df_wc = data.groupby("wc_binned").count().reset_index()
df_wc = df_wc.rename(columns={"ID":"Accident Cases", "wc_binned":"Wind Chill (F)"})
bar_wc = px.bar(df_wc, x='Wind Chill (F)', y='Accident Cases')
pie_wc = px.pie(df_wc, values='Accident Cases', names='Wind Chill (F)', color_discrete_sequence=px.colors.sequential.RdBu,hole=0.5)

##### Wind Speed ######
bins_ws, labels_ws = generate_intervals_labels('Wind_Speed(mph)', 9, 5)
data["ws_binned"] = pd.cut(data["Temperature(F)"], bins_ws, labels=labels_ws)
df_ws = data.groupby("ws_binned").count().reset_index()
df_ws = df_ws.rename(columns={"ID":"Accident Cases", "ws_binned":"Wind Speed (mph)"})
bar_ws = px.bar(df_ws, x='Wind Speed (mph)', y='Accident Cases')
pie_ws = px.pie(df_ws, values='Accident Cases', names='Wind Speed (mph)', color_discrete_sequence=px.colors.sequential.RdBu,hole=0.5)

##### Visibility ######
bins_vis, labels_vis = generate_intervals_labels('Visibility(mi)', 10, 5)
data["vis_binned"] = pd.cut(data["Temperature(F)"], bins_vis, labels=labels_vis)
df_vis = data.groupby("vis_binned").count().reset_index()
df_vis = df_vis.rename(columns={"ID":"Accident Cases", "vis_binned":"Visibility (mi)"})
bar_vis = px.bar(df_vis, x='Visibility (mi)', y='Accident Cases')
pie_vis = px.pie(df_vis, values='Accident Cases', names='Visibility (mi)', color_discrete_sequence=px.colors.sequential.RdBu,hole=0.5)



layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Weather Analysis'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Visualising trends across different weather conditions that impact the number of accident cases across the country'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Weather Conditions',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dcc.Graph(figure=weather_condition),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Temperature',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• 47% of road accidents occured in the temperature range of 41°F to 71°F'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=bar_temp), width=8),
            dbc.Col(dcc.Graph(figure=pie_temp), width=4)
        ],
        align="center",
        ),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Humidity',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• Majority of road accidents occur when the humidity is between 85% and 95%'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=bar_humi), width=8),
            dbc.Col(dcc.Graph(figure=pie_humi), width=4)
        ],
        align="center",
        ),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Pressure',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• In almost 94% of road accident cases, the pressure range is between 27 and 30 inch of mercury (inHg) '), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=bar_press), width=8),
            dbc.Col(dcc.Graph(figure=pie_press), width=4)
        ],
        align="center",
        ),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Wind Chill',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• In most of the cases, the wind chill temperature was between 56°F and 76°F'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=bar_wc), width=8),
            dbc.Col(dcc.Graph(figure=pie_wc), width=4)
        ],
        align="center",
        ),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Wind Speed',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• A positive correlation can be seen between the wind speed and road accident cases with a majority of cases occuring when the wind speed is between 40 and 45 mph'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=bar_ws), width=8),
            dbc.Col(dcc.Graph(figure=pie_ws), width=4)
        ],
        align="center",
        ),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Visibility',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• Majority of road accidents occur when the visibility is in the range of 45 to 80 miles'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=bar_vis), width=8),
            dbc.Col(dcc.Graph(figure=pie_vis), width=4)
        ],
        align="center",
        )
    ])
        
])

# app.run_server(debug=True)
