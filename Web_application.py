# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:10:46 2022

@author: rauts
"""
import numpy as np
import pandas as pd
import json
import plotly
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from flask import Flask, redirect, url_for, render_template, request

#Create an instance of class

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    data = pd.DataFrame({'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
      'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
    })
    #if request.method == 'POST':
    #    data = pd.read_csv(request.files.get('US_Accidents_Dec20_data.csv'))
    #    return render_template('index.html', shape=data.shape)
    #state_count_acc = pd.value_counts(data['State'])
    #fig = go.Figure(data=go.Choropleth(
    #locations=state_count_acc.index,
    #z = state_count_acc.values.astype(float),
    #locationmode = 'USA-states',
    #colorscale = 'Reds',
    #colorbar_title = "Count Accidents"))
    fig = px.bar(data, x='Fruit', y='Amount', color='City', 
        barmode='group')
    fig.update_layout(
        title_text = 'US Traffic Accident Dataset by State',
        geo_scope='usa',
        )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", graphJSON=graphJSON)
    
#@app.route("/admin")    
#def admin():
#    return redirect(url_for("home"))
if __name__ == "__main__":
    app.run()