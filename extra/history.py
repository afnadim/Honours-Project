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
import update_history


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

app.layout = html.Div([

                        html.Div([
                        dcc.Dropdown(id='select_financial_asset_history',
                                     options=[
                                        {'label': 'Bitcoin', 'value': 'Bitcoin'},
                                        {'label': 'Dollar', 'value': 'Dollar'},
                                        {'label': 'Pound', 'value': 'Pound'},
                                        {'label': 'Euro', 'value': 'Euro'},
                                        {'label': 'Yen', 'value': 'Yen'}         ],
                                     value='Bitcoin',
                                      #multi=True
                        ),
                        html.Div([
                        dcc.DatePickerRange(
                            id='my_date_picker',
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            #calendar_orientation='vertical',
                            min_date_allowed = dt(2018, 6, 1),
                            max_date_allowed = dt.now(),
                            start_date = dt(2018, 6, 1),
                            end_date = dt.today(),
                            show_outside_days=True
                            )],style={'display':'inline-block','verticalAlign':'top'}),
                        html.Div([
                            html.Button(
                                id='submit-button',
                                n_clicks=0,
                                children='Submit',
                                style={'fontSize':36, 'marginLeft':'5px','verticalAlign':'top'}

                            ),
                    ], style={'display':'inline-block','verticalAlign':'top'}),
                        dcc.Graph(id='my_graph6',
                                        figure={'data':[{'x':[1,2],'y':[3,1]}
                                        ],
                                        'layout':{
                                            'plot_bgcolor': colors['light blue'],
                                            'paper_bgcolor': colors['light blue'],
                                            'height': 300,
                                        },}),

                        ],className="six columns",style={'display':'inline-block','width':'45%','padding': 10})



])

#-------------------------------------------------------------------------------
#this will update the twitter sentiment of anything in the search box
@app.callback(Output('my_graph6', 'figure'),
                 [Input('submit-button', 'n_clicks')],
                 [State('select_financial_asset_history', 'value'),
                 State('my_date_picker', 'start_date'),
                 State('my_date_picker', 'end_date')]
              #events=[Event('graph-update6', 'interval')]
              )
def update_history_graph(n_clicks,select_financial_asset_history,start_date,end_date):
    return update_history.update(n_clicks,select_financial_asset_history,start_date,end_date)

    '''
    start=start_date
    end=end_date
    print(end)

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
                                        margin=dict(t=50),
                                        #plot_bgcolor=colors['background'],
                                        title=('Historical sentiment data of : '+select_financial_asset_history))}

'''


if __name__=='__main__':
    app.run_server()
