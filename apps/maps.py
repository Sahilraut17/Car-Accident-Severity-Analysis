import plotly.graph_objects as go
import pandas as pd

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = pd.read_csv(r'US_Accidents_2021_new.csv')

data1=data[['ID','Temperature(F)','Wind_Chill(F)','Humidity(%)','Visibility(mi)','Wind_Direction','Wind_Speed(mph)','Precipitation(in)','Civil_Twilight','Nautical_Twilight','Astronomical_Twilight','Weather_Condition']]
data2=data[['Severity','City','County','State','Timezone','Start_Lat','Start_Lng','End_Lat','End_Lng', 'Start_Time','Street']]
data_merged = pd.concat([data1, data2], axis=1)
data_merged['Start_Time'] = pd.to_datetime(data_merged['Start_Time'])
data_merged['Week_day'] = data_merged['Start_Time'].dt.dayofweek
data_merged['Month'] = data_merged['Start_Time'].dt.month
data_merged = data_merged.astype({'Month':'string'})
data_merged['Year'] = data_merged['Start_Time'].dt.year

#World map

#Top_states_Accident_count=data_merged.groupby('State')["ID"].count()
#Top_states_Accident_count=Top_states_Accident_count.reset_index(name='Accident_count')

#fig_worldmap = px.choropleth(Top_states_Accident_count, locations="State",locationmode="USA-states", color='Accident_count',
#                           color_continuous_scale="OrRd",
#                           scope="usa"
#                          )

#Pie Chart

#Top_10_states_accident=Top_states_Accident_count.nlargest(10,'Accident_count')


#pie_fig = px.pie(Top_10_states_accident, values='Accident_count', names='State', color_discrete_sequence=px.colors.sequential.Sunset,hole=0.5)

#bar Plot

#Bar_accident_fig = px.bar(Top_10_states_accident, x='State', y='Accident_count',
#             hover_data=['State', 'Accident_count'], color='Accident_count', color_continuous_scale='OrRd')

#Timezone and State Analysis 

#timezone_df = pd.DataFrame(data_merged['Timezone'].value_counts()).reset_index().rename(columns={'index':'Timezone', 'Timezone':'Cases'})

#pie_fig = px.pie(timezone_df, values='Cases', names='Timezone', color_discrete_sequence=px.colors.sequential.Sunset,hole=0.5)


#Grouping the States with respect to the count of accidents
#Timezone_states=data_merged.groupby(['Timezone', 'State'])["ID"].count()
#Timezone_states=Timezone_states.reset_index(name='Accident_count')
#Timezone_state_fig = px.sunburst(Timezone_states,path=['Timezone', 'State'], values='Accident_count',  hover_data=['Timezone', 'State','Accident_count' ], color='Accident_count', color_continuous_scale='OrRd')

#City Analysis
# create a dataframe of city and their corresponding accident cases

#city_df=data_merged.groupby(['Timezone', 'State','City' ])["ID"].value_counts()

#city_df = pd.DataFrame(data_merged['City'].value_counts()).reset_index().rename(columns={'index':'City', 'City':'Cases'})
#top_100_cities = pd.DataFrame(city_df.head(100))
#city_df_50 = pd.DataFrame(city_df.head(50))

#Treemap_city = px.treemap(top_100_cities, path=[px.Constant('USA'),'City'], values='Cases' ,color='Cases', color_continuous_scale='RdBu' ,hover_data=['City', 'Cases'])


#city_df_2 = pd.DataFrame(data_merged['City'].value_counts()).reset_index().rename(columns={'index':'City', 'City':'Cases'})
#top_10_cities = pd.DataFrame(city_df_2.head(10))

#pie_fig_cities = px.pie(top_10_cities, values='Cases', names='City', color_discrete_sequence=px.colors.sequential.RdBu[::-1],hole=0.5)

#Street Analysis
# create a dataframe of Street and their corresponding accident cases

#city_df=data_merged.groupby(['Timezone', 'State','City' ])["ID"].value_counts()

#Street_df = pd.DataFrame(data_merged['Street'].value_counts()).reset_index().rename(columns={'index':'Street', 'Street':'Cases'})
#top_100_Streets = pd.DataFrame(Street_df.head(100))
#city_df_50 = pd.DataFrame(city_df.head(50))

#Treemap_street = px.treemap(top_100_Streets, path=[px.Constant('USA'),'Street'], values='Cases' ,color='Cases', color_continuous_scale='YlOrBr' ,hover_data=['Street', 'Cases'])

#Street_df_2 = pd.DataFrame(data_merged['Street'].value_counts()).reset_index().rename(columns={'index':'Street', 'Street':'Cases'})
#top_15_Streets = pd.DataFrame(Street_df_2.head(15))

#Bar_street_accident_fig = px.bar(top_15_Streets, x='Street', y='Cases',
#             hover_data=['Street', 'Cases'], color='Cases', color_continuous_scale='YlOrBr')

#pie_fig_cities = px.pie(top_15_Streets, values='Cases', names='Street', color_discrete_sequence=px.colors.sequential.RdBu[::-1],hole=0.5)

layout = html.Div([
    dbc.Container([

        
        # Dropdown 

        
        # Data Overview
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Data Overview',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H4(children='In this dataset, we have different attributes like City, State, Timezone and even street for each accident records. Here we will analyze these four features based on the no. of cases for each distinct location.'), className="mb-4")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Filters',
                                     className="text-center text-light bg-dark"), body=True, color="cadetblue")
                    , className="mb-3")
        ]),


        dbc.Row([
            dbc.Col(dcc.Dropdown(
            id='Month_Dropdown',
            options=[
                {'label': 'All months', 'value': 'All'},
                {'label': 'January', 'value': '1'},
                {'label': 'February', 'value': '2'},
                {'label': 'March', 'value': '3'},
                {'label': 'April', 'value': '4'},
                {'label': 'May', 'value': '5'},
                {'label': 'June', 'value': '6'},
                {'label': 'July', 'value': '7'},
                {'label': 'August', 'value': '8'},
                {'label': 'September', 'value': '9'},
                {'label': 'October', 'value': '10'},
                {'label': 'November', 'value': '11'},
                {'label': 'December', 'value': '12'}
            ],
            value='All',
            style={'width': '100%', 'margin-left':'5px'}
            ),),

 
            dbc.Col(dcc.Dropdown(
            id='Weather_Dropdown',
            options=[
                {'label': 'All Weather', 'value': 'All_Weather'},
                {'label': 'Light Rain', 'value': 'Light Rain'},
                {'label': 'Mostly Cloudy', 'value': 'Mostly Cloudy'},
                {'label': 'Partly Cloudy', 'value': 'Partly Cloudy'},
                {'label': 'Fair', 'value': 'Fair'},
                {'label': 'Cloudy', 'value': 'Cloudy'},
                {'label': 'Fog', 'value': 'Fog'},
                {'label': 'Light Snow', 'value': 'Light Snow'},
                {'label': 'Haze', 'value': 'Haze'},
                {'label': 'Rain', 'value': 'Rain'},
                {'label': 'Windy', 'value': 'Fair / Windy'}
            ],
            value='All_Weather',
            style={'width': '100%', 'margin-left':'5px'}
            ),
            ),


        ],
   
        ),
    
        #TimeZone Analysis
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='TimeZone Accident trend Analysis in USA',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),

        dbc.Row([
            
            dbc.Col(dbc.Card(html.H4(children='The Plot gives us insights for US/Eastern, US/Central, US/Pacific and US/Mountain timezones. The plot shows the distribution of accidents for each Timezone and state. ',
                                     className="text-center text-light bg-dark"), body=True, color="grey")
            , className="mt-4 mb-4"),
            dbc.Col(dcc.Graph(id='Timezone_accidents', figure ={})),
            
        ],
        align="center",
        ),


        #State wise Analysis
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='State wise Accident trend in USA',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='State_wise_accidents', figure ={}))    
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Top 10 States for Accidents',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='Top_10_State_wise_accidents', figure ={})),
            dbc.Col(dbc.Card(html.H4(children='The Plot gives insights for the Top States prone to accidents. California(CA) has the most number of accidents followed by Florida(FL) and Texas(TX) when we consider the whole year.',
                                     className="text-center text-light bg-dark"), body=True, color="grey")
            , className="mt-4 mb-4"),
            
        ],
        align="center",
        ),

        #City wise Analysis
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='City wise Accident trend analysis in USA',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='City_wise_accidents', figure ={}))    
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Top 10 Cities with the highest number of Accidents',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),
        dbc.Row([
            
            dbc.Col(dbc.Card(html.H4(children='The Plot gives insights for the Top Cities prone to accidents. Miami is the city with highest no. of road accidents 17.2% followed by L:os Angeles with 14.4% for the year.  The Top 10 cities constitute a large amount of accident cases. Government can focus more on these states to build stricter laws and take actions to prevent accidents.',
                                     className="text-center text-light bg-dark"), body=True, color="grey")
            , className="mt-4 mb-4"),
            dbc.Col(dcc.Graph(id='Top_10_City_wise_accidents', figure ={})),
            
        ],
        align="center",
        ),


        #Street wise Analysis
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Street wise Accident trend analysis in USA',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='Street_wise_accidents', figure ={}))    
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Top 15 Streets with the highest number of Accidents',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='Top_15_Street_wise_accidents', figure ={})),
            dbc.Col(dbc.Card(html.H4(children='The Plot gives insights for the Top streets prone to accidents. Interstate 95 S and N are the most accident prone folowed by Interstate 5 N and S for the year. The Top 15 streets constitute a large amount of accident cases.',
                                     className="text-center text-light bg-dark"), body=True, color="grey")
            , className="mt-4 mb-4"),
            
            
        ],
        align="center",
        ),  

        #Severity Analysis
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Severity analysis of Accidents in USA',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id='Severity_accidents', figure ={})),
            dbc.Col(dbc.Card(html.H4(children='The Plot gives insights of the severity of accidents that takes plpace in USA. A large amount of accident populations is of Moderate Severity for the year 2021',
                                     className="text-center text-light bg-dark"), body=True, color="grey")
            , className="mt-4 mb-4"),
            
            
        ],
        align="center",
        ),  

        #Weather Analysis
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Weather analysis of Accidents in USA',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),

        dbc.Row([
            
            dbc.Col(dbc.Card(html.H4(children='The Plot gives insights of the top 10 weather contributing to accidents that takes place in USA.',
                                     className="text-center text-light bg-dark"), body=True, color="grey")
            , className="mt-4 mb-4"),
            dbc.Col(dcc.Graph(id='Weather_accidents', figure ={})),
            
            
        ],
        align="center",
        ), 

        
    ])

])

# page callbacks
# choose between condensed table and full table

# For Timezone 1
@app.callback(
    Output('Timezone_accidents', 'figure'),
    Input('Month_Dropdown', 'value'),
    Input('Weather_Dropdown', 'value')
)


def update_output(value,value2):
    if value == "All" and value2 =="All_Weather":
        data_merged_timezone = data_merged
    elif value == "All":
        data_merged_timezone = data_merged[data_merged['Weather_Condition'] == value2]        
    elif value2 == "All_Weather":
        data_merged_timezone = data_merged[data_merged['Month'] == value]
    else:
        data_merged_timezone_2 = data_merged[data_merged['Weather_Condition'] == value2]
        data_merged_timezone = data_merged_timezone_2[data_merged_timezone_2['Month'] == value]
    #Grouping the States with respect to the count of accidents
    Timezone_states=data_merged_timezone.groupby(['Timezone', 'State'])["ID"].count()
    Timezone_states=Timezone_states.reset_index(name='Accident_count')
    Timezone_state_fig = px.sunburst(Timezone_states,path=['Timezone', 'State'], values='Accident_count',  hover_data=['Timezone', 'State','Accident_count' ], color='Accident_count', color_continuous_scale='OrRd')
    return Timezone_state_fig 

# For Statewise Country Chart 2
@app.callback(
    Output('State_wise_accidents', 'figure'),
    Input('Month_Dropdown', 'value'),
    Input('Weather_Dropdown', 'value')
)


def update_output(value,value2):
    if value == "All" and value2 =="All_Weather":
        data_merged_Map = data_merged
    elif value == "All":
        data_merged_Map = data_merged[data_merged['Weather_Condition'] == value2]        
    elif value2 == "All_Weather":
        data_merged_Map = data_merged[data_merged['Month'] == value]
    else:
        data_merged_Map_2 = data_merged[data_merged['Weather_Condition'] == value2]
        data_merged_Map = data_merged_Map_2[data_merged_Map_2['Month'] == value]
    
    Top_states_Accident_count=data_merged_Map.groupby('State')["ID"].count()
    Top_states_Accident_count=Top_states_Accident_count.reset_index(name='Accident_count')

    fig_worldmap = px.choropleth(Top_states_Accident_count, locations="State",locationmode="USA-states", color='Accident_count',color_continuous_scale="OrRd",scope="usa")
    
    return fig_worldmap 

# For Top 10 Statewise Country Chart 3
@app.callback(
    Output('Top_10_State_wise_accidents', 'figure'),
    Input('Month_Dropdown', 'value'),
    Input('Weather_Dropdown', 'value')
)


def update_output(value,value2):
    if value == "All" and value2 =="All_Weather":
        data_merged_Map_10 = data_merged
    elif value == "All":
        data_merged_Map_10 = data_merged[data_merged['Weather_Condition'] == value2]        
    elif value2 == "All_Weather":
        data_merged_Map_10 = data_merged[data_merged['Month'] == value]
    else:
        data_merged_Map_10_2 = data_merged[data_merged['Weather_Condition'] == value2]
        data_merged_Map_10= data_merged_Map_10_2[data_merged_Map_10_2['Month'] == value]
    #Grouping the States with respect to the count of accidents
    Top_states_Accident_count=data_merged_Map_10.groupby('State')["ID"].count()
    Top_states_Accident_count=Top_states_Accident_count.reset_index(name='Accident_count')
    Top_10_states_accident=Top_states_Accident_count.nlargest(10,'Accident_count')


    Bar_accident_fig = px.bar(Top_10_states_accident, x='State', y='Accident_count',hover_data=['State', 'Accident_count'], color='Accident_count', color_continuous_scale='OrRd')
    return Bar_accident_fig

# For City Heatmap Chart 4
@app.callback(
    Output('City_wise_accidents', 'figure'),
    Input('Month_Dropdown', 'value'),
    Input('Weather_Dropdown', 'value')
)


def update_output(value,value2):
    if value == "All" and value2 =="All_Weather":
        data_merged_cities = data_merged
    elif value == "All":
        data_merged_cities = data_merged[data_merged['Weather_Condition'] == value2]        
    elif value2 == "All_Weather":
        data_merged_cities = data_merged[data_merged['Month'] == value]
    else:
        data_merged_cities_2 = data_merged[data_merged['Weather_Condition'] == value2]
        data_merged_cities = data_merged_cities_2[data_merged_cities_2['Month'] == value]
    #Grouping the States with respect to the count of accidents
    city_df = pd.DataFrame(data_merged_cities['City'].value_counts()).reset_index().rename(columns={'index':'City', 'City':'Cases'})
    top_100_cities = pd.DataFrame(city_df.head(100))
    #city_df_50 = pd.DataFrame(city_df.head(50))

    Treemap_city = px.treemap(top_100_cities, path=[px.Constant('USA'),'City'], values='Cases' ,color='Cases', color_continuous_scale='RdBu' ,hover_data=['City', 'Cases'])

    
    return Treemap_city

# For Top 10 City Donut Chart 5
@app.callback(
    Output('Top_10_City_wise_accidents', 'figure'),
    Input('Month_Dropdown', 'value'),
    Input('Weather_Dropdown', 'value')
)


def update_output(value,value2):
    if value == "All" and value2 =="All_Weather":
        data_merged_cities_10 = data_merged
    elif value == "All":
        data_merged_cities_10 = data_merged[data_merged['Weather_Condition'] == value2]        
    elif value2 == "All_Weather":
        data_merged_cities_10 = data_merged[data_merged['Month'] == value]
    else:
        data_merged_cities_10_2 = data_merged[data_merged['Weather_Condition'] == value2]
        data_merged_cities_10 = data_merged_cities_10_2[data_merged_cities_10_2['Month'] == value]
    #Grouping the States with respect to the count of accidents
    city_df_2 = pd.DataFrame(data_merged_cities_10['City'].value_counts()).reset_index().rename(columns={'index':'City', 'City':'Cases'})
    top_10_cities = pd.DataFrame(city_df_2.head(10))

    pie_fig_cities = px.pie(top_10_cities, values='Cases', names='City', color_discrete_sequence=px.colors.sequential.RdBu[::-1],hole=0.5)
    
    return pie_fig_cities

# For Street Heatmap Chart 6
@app.callback(
    Output('Street_wise_accidents', 'figure'),
    Input('Month_Dropdown', 'value'),
    Input('Weather_Dropdown', 'value')
)


def update_output(value,value2):
    if value == "All" and value2 =="All_Weather":
        data_merged_Street = data_merged
    elif value == "All":
        data_merged_Street = data_merged[data_merged['Weather_Condition'] == value2]        
    elif value2 == "All_Weather":
        data_merged_Street = data_merged[data_merged['Month'] == value]
    else:
        data_merged_Street_2 = data_merged[data_merged['Weather_Condition'] == value2]
        data_merged_Street = data_merged_Street_2[data_merged_Street_2['Month'] == value]
    #Grouping the States with respect to the count of accidents
    Street_df = pd.DataFrame(data_merged_Street['Street'].value_counts()).reset_index().rename(columns={'index':'Street', 'Street':'Cases'})
    top_100_Streets = pd.DataFrame(Street_df.head(100))
    #city_df_50 = pd.DataFrame(city_df.head(50))

    Treemap_street = px.treemap(top_100_Streets, path=[px.Constant('USA'),'Street'], values='Cases' ,color='Cases', color_continuous_scale='YlOrBr' ,hover_data=['Street', 'Cases'])

    return Treemap_street 

# For Top 15 Street Barchart Chart 7
@app.callback(
    Output('Top_15_Street_wise_accidents', 'figure'),
    Input('Month_Dropdown', 'value'),
    Input('Weather_Dropdown', 'value')
)


def update_output(value,value2):
    if value == "All" and value2 =="All_Weather":
        data_merged_Street_15 = data_merged
    elif value == "All":
        data_merged_Street_15 = data_merged[data_merged['Weather_Condition'] == value2]        
    elif value2 == "All_Weather":
        data_merged_Street_15 = data_merged[data_merged['Month'] == value]
    else:
        data_merged_Street_15_2 = data_merged[data_merged['Weather_Condition'] == value2]
        data_merged_Street_15 = data_merged_Street_15_2[data_merged_Street_15_2['Month'] == value]
    #Grouping the States with respect to the count of accidents
    Street_df_2 = pd.DataFrame(data_merged_Street_15['Street'].value_counts()).reset_index().rename(columns={'index':'Street', 'Street':'Cases'})
    top_15_Streets = pd.DataFrame(Street_df_2.head(15))

    Bar_street_accident_fig = px.bar(top_15_Streets, x='Street', y='Cases',hover_data=['Street', 'Cases'], color='Cases', color_continuous_scale='YlOrBr')
    
    return Bar_street_accident_fig 

# Severity Chart 8
@app.callback(
    Output('Severity_accidents', 'figure'),
    Input('Month_Dropdown', 'value'),
    Input('Weather_Dropdown', 'value')
)


def update_output(value,value2):
    if value == "All" and value2 =="All_Weather":
        data_merged_Severity = data_merged
    elif value == "All":
        data_merged_Severity = data_merged[data_merged['Weather_Condition'] == value2]        
    elif value2 == "All_Weather":
        data_merged_Severity = data_merged[data_merged['Month'] == value]
    else:
        data_merged_Severity_2 = data_merged[data_merged['Weather_Condition'] == value2]
        data_merged_Severity = data_merged_Severity_2[data_merged_Severity_2['Month'] == value]
    #Grouping the States with respect to the count of accidents
    Severity_df=  pd.DataFrame(data_merged_Severity['Severity'].value_counts()).reset_index().rename(columns={'index':'Severity', 'Severity':'Cases'})
    

    Severity_accident_fig = fig = px.funnel(Severity_df, y='Cases', x='Severity', color_discrete_sequence=px.colors.sequential.RdBu[::-1], orientation ='h')
    
    return Severity_accident_fig


# Weather Chart 8
@app.callback(
    Output('Weather_accidents', 'figure'),
    Input('Month_Dropdown', 'value'),
    Input('Weather_Dropdown', 'value')
)


def update_output(value,value2):
    if value == "All" and value2 =="All_Weather":
        data_merged_Weather = data_merged
    elif value == "All":
        data_merged_Weather = data_merged[data_merged['Weather_Condition'] == value2]        
    elif value2 == "All_Weather":
        data_merged_Weather = data_merged[data_merged['Month'] == value]
    else:
        data_merged_Weather_2 = data_merged[data_merged['Weather_Condition'] == value2]
        data_merged_Weather = data_merged_Weather_2[data_merged_Weather_2['Month'] == value]


    weather_condition_df = pd.DataFrame(data_merged_Weather.Weather_Condition.value_counts().head(10)).reset_index().rename(columns={'index':'Weather_Condition', 'Weather_Condition':'Cases'})
    Bar_weather_fig = px.bar(weather_condition_df, x='Weather_Condition', y='Cases',hover_data=['Weather_Condition', 'Cases'], color='Weather_Condition')
  
    
    return Bar_weather_fig
#app.run_server(debug=True)
