import sqlite3
import pandas as pd
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
    df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 100000", conn ,params=('%' + selected_asset + '%',))
    x=0
    y=0
    z=0
    #pie_sentiment_list=df['sentiment']
    #print(pie_sentiment_list)
    for i in range(100):
            if  df.sentiment.values[i] > 0.0:
                x+=1
            elif df.sentiment.values[i] < 0.0:
                y+=1
            else:
                z+=1
    fig = {
        'data': [{'labels': ['Positive', 'Negative','Neutral',],
                  'values': [x,y,z],
                  'type': 'pie',
                  'marker':{'colors':['green','red','deep blue']}
                  }],
        'layout': {
                'width':'450',
                #width=695,
                'height':'300',
                'autosize':'False',
                'margin':go.layout.Margin(l=30,r=30,b=50,t=70,pad=5),

        'font':dict(family='Courier New, monospace', size=11, color='blue'),
        'title': 'Overall Twitter Sentiment of : '+selected_asset}
         }
    return fig
