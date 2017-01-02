from flask import Flask, render_template, request, redirect

import numpy as np
import pandas as pd
import simplejson as json
import requests

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.resources import CDN
from bokeh.embed import components

app = Flask(__name__)
app.vars = {}

@app.route('/')
def main():
    return redirect('/index')
    
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    else:  
        app.vars['name'] = request.form['symbol'].upper()
        app.vars['price_type'] = request.form.getlist('pt')
        return redirect('/graph')

@app.route('/graph', methods = ['GET'] )
def graph():
    request = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=20161201&date.lt=20161230&ticker='+app.vars['name']+'&api_key=g8u9NEQHYzuXWNQupgr8')
    raw = json.loads(request.text)
    col = pd.DataFrame(raw['datatable']['columns'])
    col2 = pd.Series(col['name'])
    df = pd.DataFrame(raw['datatable']['data'], columns = col2)
    def datetime(x):
         return np.array(x, dtype=np.datetime64) 
        
    p1 = figure(x_axis_type="datetime", title="Stock Prices for " '%s' % (app.vars['name']))
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'    
        
    c = 0
    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2"]
    for i in app.vars['price_type']:
        p1.line(datetime(df['date']), df[i], color= colors[c], legend= str(i))
        c += 1
        p1.legend.location = "top_left"
    
    script, div = components(p1, CDN)    
    return render_template('graph.html', script= script, div=div, stock_name = app.vars['name'])
    

if __name__ == '__main__':
    debug = True
    app.run()
