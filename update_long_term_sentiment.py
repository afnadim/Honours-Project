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
    df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 100000", conn ,params=('%' + selected_asset + '%',))
    df.sort_values('unix', inplace=True)
    avarage=int(len(df)/3)
    #creating a dataframe with one third of the current database
    df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/3)).mean()
    #print(avarage)
    X = df.unix.values[-10:]
    Y = df.sentiment_smoothed.values[-10:]
    #Y = df.sentiment.values[-5:]
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
                                        margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=5),
                                        autosize=False,
                                        xaxis=dict(
                                            #range=[min(X),max(X)],
                                            title='Time'
                                            ),

                                        yaxis=dict(
                                                range=[min(Y)-.2,max(Y)+.2],
                                                title='Sentiment Level'
                                                ),
                                        hovermode='closest',

                                        #plot_bgcolor=colors['background'],
                                        font=dict(family='Courier New, monospace', size=11, color='blue'),
                                        title=('Long term Twitter emotion of : '+selected_asset+'<br>'+
                                        ' Based on the Average of last :'+str(avarage)+' Tweets'))}
