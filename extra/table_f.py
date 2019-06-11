import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import sqlite3
from dash.dependencies import Input,Output,State,Event
import plotly.graph_objs as go
import plotly.figure_factory as ff
#import dash_table_experiments as dt
import plotly.offline as pyo
import numpy as np


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



app = dash.Dash()

app.layout = html.Div([
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
                dcc.Interval(
                    id='graph-update5',
                    interval=1*3000 #update in every 5 seconds
                    ),
                dcc.Graph(id='my-table',
                    figure = {'data':[
                            go.Table(
                            )],
                    'layout':go.Layout(title='Live Tweets')})
            ],style={'display':'inline-block','width':'45%',
                    'border': 'solid','border-width': '0.0px','border-color':'aqua'})


@app.callback(Output('my-table','figure'),
             [Input(component_id='select_financial_asset', component_property='value')],
             events=[Event('graph-update5', 'interval')])
def table_update(select_financial_asset):
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 5", conn ,params=('%' + select_financial_asset + '%',))
    df.sort_values('unix', inplace=True)
    print(df)
    vals=[]
    for i in range(5):
        vals.append(df.sentiment.values[i])
    print(vals)
    trace = go.Table(
        columnwidth=[0.2, 0.7, 0.2],
        header=dict(
            #values=list(df.columns[1:]),
            values=['Time', 'Tweets', 'Sentiment'],
            font=dict(size=14),
            line = dict(color='#0000FF'),
            align = 'left',
            fill = dict(color=' #7fb3d5'),
        ),

        cells=dict(
            values=[df[k].tolist() for k in df.columns[0:]],
            line = dict(color='#0000FF'),
            font=dict(size=12),
            align = 'left',
            fill = dict(
            color=[[
            '#abebc6' if val>0 else
            '#f1948a' if val<0
            else '#eaeded'
            for val in vals
            ] ])))
    data = [trace]
    layout=go.Layout(title='Live Tweets related to :'+select_financial_asset)
    fig= go.Figure(data=data,layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
