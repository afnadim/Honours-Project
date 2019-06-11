#######
# Objective: build a dashboard that imports OldFaithful.csv
# from the data directory, and displays a scatterplot.
# The field names are:
# 'D' = date of recordings in month (in August),
# 'X' = duration of the current eruption in minutes (to nearest 0.1 minute),
# 'Y' = waiting time until the next eruption in minutes (to nearest minute).
######

# Perform imports here:
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as pyo
import sqlite3
from dash.dependencies import Input,Output,State,Event


# Launch the application:
app=dash.Dash()

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




app.layout=html.Div([

                html.H1(
                    children='Select a Financial Asset',
                    style={
                        'textAlign': 'marginLeft',
                        'color': colors['white'],
                        'fontSize':24
                    }
                ),
                    dcc.Dropdown(id='select_financial_asset',
                                 options=[
                                    {'label': 'Bitcoin', 'value': 'Bitcoin'},
                                    {'label': 'Dollar', 'value': 'Dollar'},
                                    {'label': 'Pound', 'value': 'Pound'},
                                    {'label': 'Euro', 'value': 'Euro'},
                                    {'label': 'Yen', 'value': 'Yen'}         ],
                                  value='Bitcoin',
                                  #multi=True
                    ),
                dcc.Graph(id='pie_chart',
                            figure = {
                                'data': [{'labels': ['Positive', 'Negative','Neutral',],
                                          'values': [1,1,1],
                                          'type': 'pie'}],
                                'layout': {'title': 'Ovearall Sentiment'}
                                 }

),
                dcc.Interval(
                    id='graph-update4',
                    interval=1*1000
                ),

])


@app.callback(Output('pie_chart', 'figure'),
              [Input(component_id='select_financial_asset', component_property='value')],
              events=[Event('graph-update4', 'interval')])
def update_graph_scatter(select_financial_asset):
    bitcoin='Bitcoin'# Create a Dash layout that contains a Graph component:
    pie_sentiment_list=[]
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 100000", conn ,params=('%' + select_financial_asset + '%',))
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
                  'type': 'pie'}],
        'layout': {'title': 'Overall Twitter Sentiment of : '+select_financial_asset}
         }
    return fig







# Add the server clause:
if __name__ == '__main__':
    app.run_server()
