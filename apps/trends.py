import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html
from dash import dcc
from datetime import date
from app import app



import dash
from dash.dependencies import Input, Output
from dash import dash_table



data = pd.read_csv(r'US_Accidents_Dec20_new.csv')

data1=data[['ID','Temperature(F)','Wind_Chill(F)','Humidity(%)','Visibility(mi)','Wind_Direction','Wind_Speed(mph)','Precipitation(in)','Civil_Twilight','Nautical_Twilight','Astronomical_Twilight','Weather_Condition']]
data2=data[['Severity','City','County','State','Timezone','Start_Lat','Start_Lng','End_Lat','End_Lng', 'Start_Time']]
data_merged = pd.concat([data1, data2], axis=1)
data_merged['Start_Time'] = pd.to_datetime(data_merged['Start_Time'])
data_merged['Week_day'] = data_merged['Start_Time'].dt.dayofweek
data_merged['Month'] = data_merged['Start_Time'].dt.month
data_merged['Year'] = data_merged['Start_Time'].dt.year

#Grouping the months with respect to the count of accidents
Top_states_month=data_merged.groupby(['Month'])["ID"].count()
Top_states_accident_month=Top_states_month.reset_index(name='Accident_count')


#Grouping the States with respect to the count of accidents
Top_states=data_merged.groupby(['Weather_Condition', 'State'])["ID"].count()
Top_states_accident=Top_states.reset_index(name='Accident_count')


#Severity Pie
df_sev_2 = data_merged.groupby(['Severity'])['Severity'].count()
df_sev=df_sev_2.reset_index(name='Severity_count')


pie_fig_severity =px.pie(df_sev, values='Severity_count', names='Severity')



Top_states_without_weather=data_merged.groupby('State')["ID"].count()
Top_states_without_weather_2=Top_states_without_weather.reset_index(name='Accident_count')

#Taking the top 10
Top_10_states_accident=Top_states_accident.nlargest(10,'Accident_count')
Top_10_states_accident_without_weather=Top_states_without_weather_2.nlargest(10,'Accident_count')

pie_fig = px.pie(Top_10_states_accident_without_weather, values='Accident_count', names='State')


#World map
fig_map = px.choropleth(Top_states_without_weather_2, locations="State",locationmode="USA-states", color='Accident_count',
                           color_continuous_scale="Viridis",
                           scope="usa"
                          )

layout = html.Div([
    dbc.Container([
       dbc.Row([
            dbc.Col(html.H1(children='US Car Accidents at a glance'), className="mb-2")
        ]),
       dbc.Row([
            dbc.Col(html.H6(children='Visualising trends across the country'), className="mb-4")
        ]),

       #Severity pie Chart
       dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Types of Severity',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
       dcc.Graph(figure=pie_fig_severity),

       dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='State vs Number of Accidents',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
       dcc.Graph(figure=pie_fig),

       #world Map
       dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='State vs Number of Accidents Map',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
       dcc.Graph(figure=fig_map),

       dcc.Dropdown(
        id='Weather_Condition_Dropdown',
        options=[
            {'label': 'Fair', 'value': 'Fair'},
            {'label': 'Light Rain', 'value': 'Light Rain'},
            {'label': 'Mostly Cloudy', 'value': 'Mostly Cloudy'},
            {'label': 'Partly Cloudy', 'value': 'Partly Cloudy'}
        ],
        value='Fair',
        style={'width': '65%', 'margin-left':'5px'}
        ),


       dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='State vs Number of Accidents',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dcc.Graph(id='State_accidents', figure ={}),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='State vs Number of Accidents',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": Top_10_states_accident_without_weather["State"],
                        "y": Top_10_states_accident_without_weather["Accident_count"],
                        "type": "bar"    
                    },
                ],
                "layout": {
                    "xaxis": {"title":"State",},
                    "yaxis": {"title":"Accidents"}
                },
            },
        ),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Monthly Accidents trends',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": Top_states_accident_month["Month"],
                        "y": Top_states_accident_month["Accident_count"],
                        "type": "bar"    
                    },
                ],
                "layout": {
                    "xaxis": {"title":"Month",},
                    "yaxis": {"title":"Accidents"}
                },
            },
        )
        
    ])
        
])

# page callbacks

@app.callback(
    Output('State_accidents', 'figure'),
    Input('Weather_Condition_Dropdown', 'value')
)


def update_output(value):
    data_States = Top_10_states_accident[Top_10_states_accident['Weather_Condition'] == value]
    barchart1 = px.bar(
        data_frame=data_States[['State','Accident_count']],
        x='State',
        y='Accident_count'
        #title='State vs Number of Accidents',
        #color='Accident_count'
    )
    return barchart1 


#app.run_server(debug=True)