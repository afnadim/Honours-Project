import time
import datetime
import plotly.graph_objs as go
import sqlite3
import pandas as pd

#colors
colors = {
    'background': ' #050505',
    'light blue': '#7FDBFF',
    'red': '#FF0000',
    'aqua': '#00FFFF',
    'green': '#008000',
    'blue': '#0000FF',
    'white':'#edf4f4',
    'deep blue':'#4333ff'
}

def update_sentiment(selected_asset):
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 10000", conn ,params=('%' + selected_asset + '%',))
    df.sort_values('unix', inplace=True)
    X = df.unix.values[-10:]
    #Y = df.sentiment_smoothed.values[-10:]
    Y = df.sentiment.values[-10:]
    data = go.Scatter(
            x=X,
            y=Y,
            name='Scatter',
            mode= 'lines+markers',
            #mode= 'lines',
            fillcolor=colors['blue'],
            marker = dict(      # change the marker style
                    size = 2,
                    color = colors['light blue'],
                    #symbol = 'pentagon',
                    line = dict(
                        width = 2,)))


    #return fig
    return {'data': [data],'layout' : go.Layout(

                                        width=450,
                                        #width=695,
                                        height=300,
                                        autosize=False,
                                        xaxis=dict(
                                        #range=[min(X),max(X)],
                                        title='Time'),

                                        yaxis=dict(
                                                range=[min(Y)-.2,max(Y)+.2],
                                                title='Sentiment Level'
                                                ),
                                        hovermode='closest',
                                        margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=5),
                                        #plot_bgcolor=colors['background'],
                                        font=dict(family='Courier New, monospace', size=11, color='blue'),
                                        title=('Live Twitter emotion of : '+selected_asset))}
