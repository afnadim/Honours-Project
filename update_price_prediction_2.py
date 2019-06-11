import sqlite3
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

#setting customise colors for the application
colors = {
    'background': ' #050505',
    'light blue': '#7FDBFF',
    'red': '#660000',
    'aqua': '#00FFFF',
    'green': '#008000',
    'blue': '#0000FF',
    'white':'#edf4f4',
    'deep blue':'#4333ff'
}

def update(selected_asset):
    bitcoin='Bitcoin'# Create a Dash layout that contains a Graph component:
    pie_sentiment_list=[]
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    #df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 10000", conn ,params=('%' + selected_asset + '%',))

    #reading first 2000 instances from the dataset
    df = pd.read_sql("SELECT * FROM sentiment ORDER BY unix DESC LIMIT 200", conn)
    #df = pd.read_sql_query("select * from sentiment limit 2000;", conn)
    #sliceing the database into 2

    df1=df[:100]
    df2=df[100:]
    #number of time selected financial asset mentioned in each update_asset_price
    #num1=df1['tweet'].str.contains(selected_asset)

    df3=df1.set_index('tweet').filter(regex=selected_asset, axis=0)
    df4=df2.set_index('tweet').filter(regex=selected_asset, axis=0)
    #print(len(df))
    #print(len(df1))
    #print(len(df2))
    #print(len(df3))
    #print(len(df4))

    #print(df1.head)
    #print(df2.head)
    #print(df.head)
    x=len(df3)
    y=len(df4)
    #pie_sentiment_list=df['sentiment']
    #print(pie_sentiment_list)
    fig = {
        'data' : [go.Bar(
            x=['current volume', 'previous volume'],
            y=[x,y],

            #orientation = 'h'
            )],
        'layout': {
                'width':'450',
                #width=695,
                'height':'300',
                'autosize':'False',
                'margin':go.layout.Margin(l=30,r=30,b=30,t=70,pad=5),

        'font':dict(family='Courier New, monospace', size=11, color='blue'),
        'title': 'Volume of Tweets related to  : '+selected_asset +'<br>'+'Volume size : 100' }
         }

    return fig
