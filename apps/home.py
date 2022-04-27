from dash import html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Car Accident Severity Analysis", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='The economic and social impact of road accidents is affecting U.S. citizens. Road crashes cost the U.S. $230.6 billion per year or an average of $820 per person. Reducing road accidents, especially the worst accidents, however, remains an important challenge. The acceleration method, one of the two main ways to deal with road safety problems, focuses on preventing unsafe road conditions from happening in the first place. For effective use of this method, risk forecasting and difficulty forecasting are essential. If we can identify patterns of how these bad accidents occur and the key factors, we can take informed actions and better share financial and human resources.'
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='The primary objective of this dashboard is to recognize key factors contributing to road accidents, without any detailed information about itself, like driver attributes or vehicle type. This visualization is supposed to be able to find the pattern of the accident in the United States. This dashboard aims to demonstrate information about accidents and discover patterns with respect to weather conditions, location, and time of the year.')
                    , className="mb-5")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(children=[html.H3(children='Get the original dataset used in this dashboard',
                                               className="text-center"),
                                       dbc.Row([dbc.Col(dbc.Button("Dataset", href="https://www.kaggle.com/sobhanmoosavi/us-accidents",
                                                                   color="primary"),
                                                        className="d-grid gap-2"),
                                                ], justify="center")
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-6"),

            dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                               className="text-center"),
                                       dbc.Row([dbc.Col(dbc.Button("GitHub", href="https://github.com/Sahilraut17/Car-Accident-Severity-Analysis",
                                                                   color="primary"),
                                                        className="d-grid gap-2"),
                                                ], justify="center")
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-6"),
        ], className="mb-3"),
    ])

])

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)
