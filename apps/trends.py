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



data = pd.read_csv(r'US_Accidents_2021_new.csv')

data1=data[['ID','Temperature(F)','Wind_Chill(F)','Humidity(%)','Visibility(mi)','Wind_Direction','Wind_Speed(mph)','Precipitation(in)','Civil_Twilight','Nautical_Twilight','Astronomical_Twilight','Weather_Condition']]
data2=data[['Severity','City','County','State','Timezone','Start_Lat','Start_Lng','End_Lat','End_Lng', 'Start_Time', 'End_Time']]
data3=data[['Bump', 'Crossing', 'Give_Way', 'Junction', 'Stop', 'No_Exit', 'Traffic_Signal', 'Turning_Loop']]
data_merged = pd.concat([data1, data2], axis=1)
data_merged['Start_Time'] = pd.to_datetime(data_merged['Start_Time'])
data_merged['Week_day'] = data_merged['Start_Time'].dt.dayofweek
data_merged['Month'] = data_merged['Start_Time'].dt.month
data_merged['Year'] = data_merged['Start_Time'].dt.year


data['Start_Time'] = pd.to_datetime(data['Start_Time'])
data['Start_Time2'] = pd.to_datetime(data['Start_Time2'])
data['End_Time'] = pd.to_datetime(data['End_Time'])



# Accident Duration Analysis
accident_duration_df = pd.DataFrame(data['End_Time'] - data['Start_Time2']).reset_index().rename(columns={'index':'Id', 0:'Duration'})
top_10_accident_duration_df = pd.DataFrame(accident_duration_df['Duration'].value_counts().head(10).sample(frac = 1)).reset_index().rename(columns={'index':'Duration', 'Duration':'Accident Cases'})
Duration = [str(i).split('days')[-1].strip() for i in top_10_accident_duration_df.Duration]
top_10_accident_duration_df['Duration'] = Duration
acc_duration_bar = px.bar(top_10_accident_duration_df, x='Duration', y='Accident Cases', color='Accident Cases', color_continuous_scale='Emrld')


# Monthly Analysis
monthly_df =data_merged.groupby(['Month'])["ID"].count().reset_index(name='Accident_count')
monthly_df = monthly_df.rename(columns={"Accident_count":"Accident Cases"})
monthly_bar = px.bar(monthly_df, x='Month', y='Accident Cases', color='Accident Cases', color_continuous_scale='Emrld')
monthly_pie = px.pie(monthly_df, values='Accident Cases', names='Month', color_discrete_sequence=px.colors.sequential.Emrld[::-1],hole=0.5)

# Day Analysis
day_df = pd.DataFrame(data.Start_Time.dt.day_name().value_counts()).reset_index().rename(columns={'index':'Day', 'Start_Time':'Accident Cases'})
day_bar = px.bar(day_df, x='Day', y='Accident Cases', color='Accident Cases', color_continuous_scale='deep')
day_pie = px.pie(day_df, values='Accident Cases', names='Day', color_discrete_sequence=px.colors.sequential.deep[::-1],hole=0.5)


# Hour Analysis
hour_df = pd.DataFrame(data.Start_Time2.dt.hour.value_counts()).reset_index().rename(columns={'index':'Hours', 'Start_Time2':'Accident Cases'}).sort_values('Hours')
hour_bar = px.bar(hour_df, x='Hours', y='Accident Cases', color='Accident Cases', color_continuous_scale='Emrld')
hour_pie = px.pie(hour_df, values='Accident Cases', names='Hours', color_discrete_sequence=px.colors.sequential.Emrld[::-1],hole=0.5)



layout = html.Div([
    dbc.Container([
       dbc.Row([
            dbc.Col(html.H1(children='Time Analysis'), className="mb-2")
        ]),
       dbc.Row([
            dbc.Col(html.H5(children='An Analysis on the number of accident cases based on month of year, day, and hour'), className="mb-4")
        ]),
       dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Accident Duration Analysis',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
       dbc.Row([
            dbc.Col(html.H5(children='• Majority of road accident cases have impacted the traffic flow for around 1.5 hours'), className="mb-4")
        ]),
       dcc.Graph(figure=acc_duration_bar),


       dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Month Analysis',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• Around 18% of the road accidents occurred in the month of December'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• March observed the least (4.34%) number of road accidents in the US'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• Almost 40% of the road accidents occurred within 3 months from October to December (i.e., transition period from Autumn to Winter)'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=monthly_bar), width=8),
            dbc.Col(dcc.Graph(figure=monthly_pie), width=4)
        ],
        align="center",
        ),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Day Analysis',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• Working days of the week have a higher number of cases, compared to the weekend'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• Sunday has the lowest number of cases at around 10%'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• Friday has the highest percentage of road accidents at 17.5%'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=day_bar), width=8),
            dbc.Col(dcc.Graph(figure=day_pie), width=4)
        ],
        align="center",
        ),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Hour Analysis',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• Around 16% of the road accidents occurred between 6:00AM and 9:00AM'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• Most of the accidents occurred during evening office-returning hours, between 3:00PM and 6:00PM'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• As for morning hours, most accidents occured between 7:00AM and 8:00AM implying morning office-going hours'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=hour_bar), width=8),
            dbc.Col(dcc.Graph(figure=hour_pie), width=4)
        ],
        align="center",
        ),

       dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Road Condition Analysis',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4")
       ]),
       dcc.Dropdown(
        id='Road_Condition_Dropdown',
        options=[
            {'label': 'Bump', 'value': 'Bump'},
            {'label': 'Crossing', 'value': 'Crossing'},
            {'label': 'Give Way', 'value': 'Give_Way'},
            {'label': 'Junction', 'value': 'Junction'},
            {'label': 'Stop', 'value': 'Stop'},
            {'label': 'No Exit', 'value': 'No_Exit'},
            {'label': 'Traffic Signal', 'value': 'Traffic_Signal'},
            {'label': 'Turning Loop', 'value': 'Turning_Loop'}
        ],
        value='Crossing',
        style={'width': '65%', 'margin-left':'5px'}
        ),
       dcc.Graph(id='road_condition', figure ={}),
       dbc.Row([
            dbc.Col(html.H5(children='• In nearly every case, a bumper was absent at the accident spot'), className="mb-4")
        ]),
       dbc.Row([
            dbc.Col(html.H5(children='• In around 7.5% cases, road accidents happened near a crossing'), className="mb-4"),
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• 6.72% road accident cases were recorded near junctions'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• In almost 98% cases, there was no Stop sign near the accident area'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• There are no accident cases recorded near turning loops'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='• Around 8% of all road accident cases happened near a traffic signal'), className="mb-4")
        ])
        
    ])
        
])

# page callbacks

@app.callback(
    Output('road_condition', 'figure'),
    Input('Road_Condition_Dropdown', 'value')
)

def update_output(value):
    dt = data3[value]
    piechart = px.pie(dt, values=dt.value_counts(), names=dt.value_counts().index, hole=0.5)

    return piechart

#app.run_server(debug=True)
