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

data = pd.read_csv(r'US_Accidents_Dec20_new.csv')

data1=data[['ID','Temperature(F)','Wind_Chill(F)','Humidity(%)','Visibility(mi)','Wind_Direction','Wind_Speed(mph)','Precipitation(in)','Civil_Twilight','Nautical_Twilight','Astronomical_Twilight','Weather_Condition']]
data2=data[['Severity','City','County','State','Timezone','Start_Lat','Start_Lng','End_Lat','End_Lng', 'Start_Time']]
data_merged = pd.concat([data1, data2], axis=1)
data_merged['Start_Time'] = pd.to_datetime(data_merged['Start_Time'])
data_merged['Week_day'] = data_merged['Start_Time'].dt.dayofweek
data_merged['Month'] = data_merged['Start_Time'].dt.month
data_merged = data_merged.astype({'Month':'string'})
data_merged['Year'] = data_merged['Start_Time'].dt.year

#World map

Top_states_Accident_count=data_merged.groupby('State')["ID"].count()
Top_states_Accident_count=Top_states_Accident_count.reset_index(name='Accident_count')

fig_worldmap = px.choropleth(Top_states_Accident_count, locations="State",locationmode="USA-states", color='Accident_count',
                           color_continuous_scale="OrRd",
                           scope="usa"
                          )

#Pie Chart

Top_10_states_accident=Top_states_Accident_count.nlargest(10,'Accident_count')


pie_fig = px.pie(Top_10_states_accident, values='Accident_count', names='State', color_discrete_sequence=px.colors.sequential.Sunset,hole=0.5)

#bar Plot

Bar_accident_fig = px.bar(Top_10_states_accident, x='State', y='Accident_count',
             hover_data=['State', 'Accident_count'], color='Accident_count', color_continuous_scale='OrRd')

#Timezone and State Analysis 

timezone_df = pd.DataFrame(data_merged['Timezone'].value_counts()).reset_index().rename(columns={'index':'Timezone', 'Timezone':'Cases'})

#pie_fig = px.pie(timezone_df, values='Cases', names='Timezone', color_discrete_sequence=px.colors.sequential.Sunset,hole=0.5)


#Grouping the States with respect to the count of accidents
Timezone_states=data_merged.groupby(['Timezone', 'State'])["ID"].count()
Timezone_states=Timezone_states.reset_index(name='Accident_count')
Timezone_state_fig = px.sunburst(Timezone_states,path=['Timezone', 'State'], values='Accident_count',  hover_data=['Timezone', 'State','Accident_count' ], color='Accident_count', color_continuous_scale='OrRd')

#City Analysis
# create a dataframe of city and their corresponding accident cases

#city_df=data_merged.groupby(['Timezone', 'State','City' ])["ID"].value_counts()

city_df = pd.DataFrame(data_merged['City'].value_counts()).reset_index().rename(columns={'index':'City', 'City':'Cases'})
#city_df_50 = pd.DataFrame(city_df.head(50))

Treemap_city = px.treemap(city_df, path=[px.Constant('USA'),'City'], values='Cases' ,color='Cases', color_continuous_scale='RdBu' ,hover_data=['City', 'Cases'])


city_df_2 = pd.DataFrame(data_merged['City'].value_counts()).reset_index().rename(columns={'index':'City', 'City':'Cases'})
top_10_cities = pd.DataFrame(city_df_2.head(10))

pie_fig_cities = px.pie(top_10_cities, values='Cases', names='City', color_discrete_sequence=px.colors.sequential.RdBu[::-1],hole=0.5)

layout = html.Div([
    dbc.Container([

        

        # Data Overview
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Data Overview',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H4(children='In this dataset, we have different attributes like City, State, Timezone and even street for each accident records. Here we will analyze these four features based on the no. of cases for each distinct location.'), className="mb-4")
        ]),

        #TimeZone Analysis
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='TimeZone Accident trend Analysis in USA',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),

        dbc.Row([
            
            dbc.Col(dbc.Card(html.H4(children='Eastern time zone region of US has the highest no. of road accident cases while Mountain time zone region of US has the lowest no. of road accident cases',
                                     className="text-center text-light bg-dark"), body=True, color="grey")
            , className="mt-4 mb-4"),
            dbc.Col(dcc.Graph(figure=Timezone_state_fig)),
            
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
            dbc.Col(dcc.Graph(figure=fig_worldmap))    
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Top 10 States for Accidents',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=Bar_accident_fig)),
            dbc.Col(dbc.Card(html.H4(children='California(CA) has the most number of accidents followed by Florida(FL) and Texas(TX). It is interesting to see that the number of accidents in California is almost twice the number of accidents in Florida.',
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
            dbc.Col(dcc.Graph(figure=Treemap_city))    
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Top 10 States for Accidents',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mt-4 mb-4"),
            
        ]),
        dbc.Row([
            
            dbc.Col(dbc.Card(html.H4(children='Miami is the city with highest no. of road accidents 17.2% followed by L:os Angeles with 14.4%. These Cities. The Top 10 cities constitute a large amount of accident cases. Givernment can focus more on these states to build stricter laws and actions to prevent accidents.',
                                     className="text-center text-light bg-dark"), body=True, color="grey")
            , className="mt-4 mb-4"),
            dbc.Col(dcc.Graph(figure=pie_fig_cities)),
            
        ],
        align="center",
        ),

        
        
    ])

])

# page callbacks
# choose between condensed table and full table
@app.callback([Output('datatable', 'data'),
              Output('datatable', 'columns')],
             [Input('table_type', 'value')])

def update_columns(value):
    df2 = df.tail(5)
    col = ['ID', 'Source']
    df2['Severity'] = df2[col].sum(axis=1)

    condensed_col = ['ID', 'Start_Time', 'City', 'County']

    full_col = ['ID', 'Start_Time', 'City', 'County', 'Country']

    if value == 'Condensed table':
        columns = [{"name": i, "id": i} for i in condensed_col]
        data=df2.to_dict('records')
    elif value == 'Full table':
        columns = [{"name": i, "id": i} for i in full_col]
        data=df2.to_dict('records')
    return data, columns

# allow for easy sieving of data to see how the situation has changed
# can observe whether government measures are effective in reducing the number of cases
@app.callback(Output('graph_by_period', 'figure'),
              [Input('Weather', 'value')])

def update_graph(Weather_name):
    dff = df[df.Weather_Condition == Weather_name]
    # not sure why this doesn't work, Daily Confirmed is an invalid key
    col = ['Severity']
    dff['total'] = dff[col].sum(axis=1)
    data = [go.Scatter(x=dff['State'], y=dff['total'],
                       mode='markers',name='Analysis of top 5 weather Condition')]
    layout = go.Layout(
        yaxis={'title': "Accidents"},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        template = "seaborn",
        margin=dict(t=20)
    )

    return {'data': data, 'layout': layout}

@app.callback(Output('choropleth us', 'figure'),
              [Input('choropleth_us', 'value')])

def update_choropleth(Weather_name):
    dff = df[df.Weather_Condition == Weather_name]
    # not sure why this doesn't work, Daily Confirmed is an invalid key
    col = ['Severity']
    dff['total'] = dff[col].sum(axis=1)
    data = [go.Scatter(x=dff['State'], y=dff['total'],
                       mode='markers',name='Analysis of top 5 weather Condition')]
    layout = go.Layout(
        yaxis={'title': "Accidents"},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        template = "seaborn",
        margin=dict(t=20)
    )

    return {'data': data, 'layout': layout}

@app.callback([Output('local and imported', 'figure'),
               Output('dorms', 'figure')],
              [Input('graph_by_period', 'hoverData')])

def update_breakdown(hoverData):
    day = hoverData['points'][0]['x']
    dff = df[df['Date'] == day]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=dff['Date'], y=dff['Daily Local transmission'],
                          name='Local cases'))

    fig2.add_trace(go.Bar(x=dff['Date'], y=dff['Daily Imported'],
                          name='Imported cases'))

    # edit layout
    fig2.update_layout(yaxis_title='Cases',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=20))

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=dff['Date'], y=dff['Local cases residing in dorms'],
                          name='Residing in dorms'))

    fig3.add_trace(go.Bar(x=dff['Date'], y=dff['Local cases not residing in dorms'],
                          name='Not residing in dorms'))

    # edit layout
    fig3.update_layout(yaxis_title='Cases',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=20))
    return fig2, fig3

# update hospital situation graph
@app.callback(Output('situation_graph_by_period', 'figure'),
              [Input('Weather', 'value'),
               Input('choose_hospital_situation', 'value')])

def update_situation_graph(Weather_name, choose_hospital_situation_name):
    dff = df[df.Weather_Condition == Weather_name]

    trace = []

    for i in choose_hospital_situation_name:
        trace.append(go.Bar(name=i, x=dff['Date'], y=dff[i]))

    data = trace

    layout = go.Layout(
        yaxis={'title': "Cases"},
        barmode='stack',
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        template="seaborn",
        margin=dict(t=20)
    )

    return {'data': data, 'layout': layout}

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)
