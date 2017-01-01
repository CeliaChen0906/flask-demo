from flask import Flask, render_template, request, redirect

import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT
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
       
        return redirect ('/graph')
    
@app.route('/graph', methods = ['POST'])
def graph():    
    def datetime(x):   
        return np.array(x, dtype=np.datetime64)
    p1 = figure(x_axis_type="datetime", title="Stock Prices for")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    p1.line(datetime(AAPL['date']), AAPL['adj_close'], color='#A6CEE3', legend='AAPL')
    p1.line(datetime(GOOG['date']), GOOG['adj_close'], color='#B2DF8A', legend='GOOG')
    p1.line(datetime(IBM['date']), IBM['adj_close'], color='#33A02C', legend='IBM')
    p1.line(datetime(MSFT['date']), MSFT['adj_close'], color='#FB9A99', legend='MSFT')
    p1.legend.location = "top_left"
    
    script, div = components(p1, CDN)
    
    return render_template('graph.html', script= script, div=div, stock_name = 'GOOG')

if __name__ == '__main__':
    debug = True
    app.run(host='104.131.67.119')
