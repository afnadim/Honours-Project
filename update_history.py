import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State,Event
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
from pandas.api.types import is_list_like
import sqlite3
import time
import datetime
from datetime import datetime as dt
from datetime import timedelta
import plotly.graph_objs as go

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

def update(n_clicks,select_financial_asset_history,start_date,end_date):
    start=start_date
    end=end_date
    print(end)
    '''
    today=dt.today()
    #print(today)
    end_ms=str(end)
    today_ms=str(today)
    #print(end_ms)

    #giving cureent time the end date is today
    if 'end_ms'in 'today_ms':
        end=dt.now()
        print('dfdddddddddddddd')
    else:
        end=end_date
        print('sdddddddddd')
    '''

    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 10000", conn ,params=('%' + select_financial_asset_history + '%',))
    df.sort_values('unix', inplace=True)

    #print(df)

    #df = df[select_financial_asset_history,start,end]
    #df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()
    #X = df.unix.values[start<end]

    X = df.unix.values[:]
    #Y = df.sentiment_smoothed.values[-10:]
    Y = df.sentiment.values[:]


    data = go.Scatter(
            x=X,
            y=Y,

            name='Scatter',
            mode= 'lines+markers',
            text = df.tweet,
            hoverinfo = ['text','x','y'],

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
                                        height=210,
                                        autosize=False,
                                        xaxis=dict(
                                            #range=[min(X),max(X)],
                                            range = [start,end],
                                            title='Time Range'
                                            ),

                                        yaxis=dict(
                                                range=[min(Y)-.2,max(Y)+.2],
                                                title='Sentiment Level'
                                                ),
                                        hovermode='closest',
                                        margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=5),
                                        #plot_bgcolor=colors['background'],
                                        font=dict(family='Courier New, monospace', size=11, color='blue'),
                                        title=('Historical sentiment data of : '+select_financial_asset_history))}
