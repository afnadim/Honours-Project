import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State,Event
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
from datetime import datetime
from pandas.api.types import is_list_like
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from unidecode import unidecode
import time
import datetime
from datetime import datetime as dt
import plotly.graph_objs as go
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
import requests
import update_piechart
import update_asset_price
import update_current_sentiment
import update_long_term_sentiment
import update_tweet_table
import update_history
import update_price_prediction_1
import update_price_prediction_2
import update_price_prediction_3


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash()
#seeting title of the app
app.title = 'FinTweetMonitor'

app.config.supress_callback_exceptions=True
#setting customise colors for the application
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

#setting styles for the tabs
tab_style = {
    'borderBottom': 'aqua',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'blue',
    'color': 'white',
    'fontSize':16
    #'padding': '6px'
}




app.layout = html.Div([
    #this is placeholder for recurrent functions
    #dcc.Interval(id='graph-update15',interval=1*1000),
    dcc.Interval(id='interval1', interval=1 * 100000, n_intervals=0),
    html.H1(id='label1', children=''),
    html.H2(children='Twitter Sentiment Analysis of Financial Assets',
            style={'fontSize':24,'textAlign': 'center','color': ['green']}),
    #tab1 for visualise the sentiment
    dcc.Tabs(id="tabs_switch", value='tab-1', children=[
        dcc.Tab(label='Sentiment Visualisation', value='tab-1',selected_style=tab_selected_style,
            style={'fontSize':16,'backgroundColor':'green','width':'20%','color': 'deep blue'}
        ),

        #tab2 for price indicator
        dcc.Tab(label='Price Indicator', value='tab-2',selected_style=tab_selected_style,
            style={'fontSize':16,'backgroundColor':'green','width':'20%','color': 'deep blue'}
        ),
    ],colors={"border": "white","primary": "green","background": "blue"}),
    html.Div(id='tabs')
],style={'backgroundColor':'background','padding': 2})

@app.callback(Output('tabs', 'children'),
              [Input('tabs_switch', 'value')])
def render_content(tab):
    if tab == 'tab-1':
#contents of tab one
#----------------------------------------------------------
        return html.Div([
            #html.H3('Live Visualisation of twitter sentimnet'),
    #contents of tab 1
    #-------------------------------------------------------
            #html.H3('Live price prediction'),
    #-------------------------------------------------------
            #div for dropdown mwnu
            html.Div([
            html.H1(
                children='Select a Financial Asset',
                style={
                    'textAlign': 'marginLeft',
                    'marginTop':'0.0px',
                    'color': colors['white'],
                    'padding': 2,
                    'fontSize':20
                }),
            #dropdown list
            dcc.Dropdown(id='select_financial_asset',
                         options=[
                            {'label': 'Bitcoin', 'value': 'Bitcoin'},
                            {'label': 'Dollar', 'value': 'Dollar'},
                            {'label': 'Pound', 'value': 'Pound'},
                            {'label': 'Euro', 'value': 'Euro'},
                            {'label': 'Yen', 'value': 'Yen'}         ],
                          value='Bitcoin',
                          #multi=True
            )],style={'display':'inline-block','verticalAlign':'top',
            'width':'50%','padding': 5,'color': colors['blue'],}),

            #this section will hold 2 blocks to show current price and twitter emotion of the asset
            html.Div([
            #-----------------------------------------------------------------------
                #this block to show the currenct price of the asset
                html.Div([
                dcc.Graph(id='my_graph1',
                                figure={'data':[{'x':[1,2],'y':[3,1]}
                                ],
                                'layout':{
                                    'width':'400',
                                    #width=695,
                                    'height':'300',
                                    'autosize':'False',
                                    'plot_bgcolor': colors['light blue'],
                                    'paper_bgcolor': colors['light blue'],
                                    },}),
                #setting the update interval of this graph
                dcc.Interval(
                    id='graph-update1',
                    interval=1*1000
                ),
                ],className="six columns",style={'display':'inline-block',
                'width':'26%','padding': 2}),

            #-----------------------------------------------------------------------
                #this section will show the twitter emotion of the asset
                html.Div([
                dcc.Graph(id='my_graph2',
                                figure={'data':[{'x':[1,2],'y':[3,1]}
                                ],
                                'layout':{
                                    'width':'400',
                                    #width=695,
                                    'height':'300',
                                    'autosize':'False',
                                    'plot_bgcolor': colors['light blue'],
                                    'paper_bgcolor': colors['light blue'],
                                    },}),
                #update graph in a interval
                dcc.Interval(
                    id='graph-update2',
                    interval=1*1000
                ),
                ],className="six columns",style={'display':'inline-block','width':'26%','padding': 2}),

                #this will show the long term twitter emotion of the finalcial asset
                        html.Div([
                        dcc.Graph(id='my_graph3',
                                        figure={'data':[{'x':[1,2],'y':[3,1]}
                                        ],

                                        'layout':{
                                            'width':'400',
                                            #width=695,
                                            'height':'300',
                                            'autosize':'False',
                                            'plot_bgcolor': colors['light blue'],
                                            'paper_bgcolor': colors['light blue'],
                                            },}),
                        #setting the update interval
                        dcc.Interval(
                            id='graph-update3',
                            interval=1
                        ),
                        ],className="six columns",style={'display':'inline-block',
                        'width':'26%','padding': 2}),

                ], className="row"),

        #---------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------
            html.Div([

                #this div will show the latest Tweets in a table with emotion level
                html.Div([
                #setting the update interval
                dcc.Graph(id='my-table',
                    figure = {'data':[
                            go.Table(
                            )],
                    'layout':go.Layout(title='Live Tweets')}),
                dcc.Interval(
                    id='graph-update5',
                    interval=1*1000 #update in every 5 seconds
                    ),

                ],className="six columns",
                style={'display':'inline-block',
                    'width':'26%','padding': 5}),


                #this block to show the overall sentiment of the selected asset in a pie chart
                html.Div([
                dcc.Graph(id='pie_chart',
                            figure = {
                                'data': [{'labels': ['Positive', 'Negative','Neutral',],
                                          'values': [1,1,1],
                                          'type': 'pie',

                                          }],

                                'layout': {'title': 'Ovearall Sentiment'}
                                 }),
                #setting update interval time
                dcc.Interval(
                    id='graph-update4',
                    interval=1*1000
                ),
            ],className="six columns",
                style={'display':'inline-block','width':'26%',
                        'border': 'solid','border-width': '0.0px','border-color':'aqua','padding': 5}),
                #-------------------------------------------------------------------
                #this section will show the twitter emotion of any Asset

            html.Div([
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
                ),],style={'verticalAlign':'top','width':'72%','color':'blue',}),
                html.Div([
                dcc.DatePickerRange(
                    id='my_date_picker',
                    start_date_placeholder_text="Start Period",
                    end_date_placeholder_text="End Period",
                    #calendar_orientation='vertical',
                    min_date_allowed = dt(2018, 6, 1),

                    #max_date_allowed =datetime.timedelta(days = 1),
                    max_date_allowed = dt.now(),
                    start_date = dt(2019, 1, 1),
                    end_date = dt.now(),

                    show_outside_days=True
                    )],style={'display':'inline-block','verticalAlign':'top','fontSize':12,'width':'54%','color':'blue'}),
                html.Div([
                    html.Button(
                        id='submit-button',
                        n_clicks=0,
                        children='Submit',
                        style={'fontSize':12,'color':'blue',
                        'backgroundColor':'white','marginLeft':'0px'}

                        ),
                        ], style={'display':'inline-block','verticalAlign':'middle',
                        'color':'white','marginLeft':'0px'}),
                dcc.Graph(id='my_graph6',
                                figure={'data':[{'x':[1,2],'y':[3,1]}
                                ],
                                'layout':{
                                'plot_bgcolor': colors['light blue'],
                                'paper_bgcolor': colors['light blue'],
                                'height': 350,
                                },}),

                ],className="six columns",style={'display':'inline-block',
                        'width':'33%','padding': 5}),
                    ], className="row"),
                ],style={'backgroundColor': colors['background'],'padding': 25})


    elif tab == 'tab-2':
        return html.Div([
            #html.H3('Live Visualisation of twitter sentimnet'),
    #contents of tab 2
    #-------------------------------------------------------
            #html.H3('Live price prediction'),
    #-------------------------------------------------------
            #div for dropdown mwnu
            html.Div([
            html.H1(
                children='Select a Financial Asset',
                style={
                    'textAlign': 'marginLeft',
                    'color': colors['white'],
                    'fontSize':20
                }),
            #dropdown list
            dcc.Dropdown(id='select_financial_asset1',
                         options=[
                            {'label': 'Bitcoin', 'value': 'Bitcoin'},
                            {'label': 'Dollar', 'value': 'Dollar'},
                            {'label': 'Pound', 'value': 'Pound'},
                            {'label': 'Euro', 'value': 'Euro'},
                            {'label': 'Yen', 'value': 'Yen'}         ],
                          value='Bitcoin',
                          #multi=True
            )],style={'display':'inline-block','verticalAlign':'top',
            'width':'50%','padding': 5,'color': colors['blue'],}),


        #---------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------
            html.Div([

                #this block to show the overall sentiment of the selected asset in a pie chart
                html.Div([
                dcc.Graph(id='pie_chart1',
                            figure = {
                                'data': [{'labels': ['Positive', 'Negative','Neutral',],
                                          'values': [1,1,1],
                                          'type': 'pie',

                                          }],

                                'layout': {


                                'width':'400',
                                #width=695,
                                'height':'300',
                                'autosize':'False',

                                'title': 'Ovearall Sentiment'}
                                 }),
                #setting update interval time
                dcc.Interval(
                    id='graph-update7',
                    interval=1*1000
                ),
            ],className="six columns",
                style={'display':'inline-block','width':'26%',
                        'border': 'solid','border-width': '0.0px','border-color':'aqua','padding': 5}),


#--------------------------------------------------------------------------------------------------------
                #this block to show the overall sentiment of the selected asset in a pie chart
                html.Div([
                dcc.Graph(id='pie_chart2',
                            figure = {
                                'data': [{'labels': ['Positive', 'Negative','Neutral',],
                                          'values': [1,1,1],
                                          'type': 'pie',

                                          }],

                                'layout': {

                                'width':'400',
                                #width=695,
                                'height':'300',
                                'autosize':'False',
                                'title': 'Ovearall Sentiment'}
                                 }),
                #setting update interval time
                dcc.Interval(
                    id='graph-update8',
                    interval=1*1000
                ),
            ],className="six columns",
                style={'display':'inline-block','width':'26%',
                        'border': 'solid','border-width': '0.0px','border-color':'aqua','padding': 5}),

#=========================================================================================================
#this div will show the price prediction from machine learning
            html.Div([
                html.Div([
                dcc.Dropdown(id='select_financial_asset_history1',
                             options=[
                                {'label': 'Bitcoin', 'value': 'Bitcoin'},
                                {'label': 'Dollar', 'value': 'Dollar'},
                                {'label': 'Pound', 'value': 'Pound'},
                                {'label': 'Euro', 'value': 'Euro'},
                                {'label': 'Yen', 'value': 'Yen'}         ],
                             value='Bitcoin',
                              #multi=True
                ),
                ],style={'display':'inline-block','verticalAlign':'top','width':'65%','color':'blue','margin':'auto'}),


                html.Div([
                    html.Button(
                        id='submit-button1',
                        n_clicks=0,
                        children='Submit',
                        style={'fontSize':14,'color':'blue','backgroundColor':'white'}

                        ),
                        ], style={'width':'30%','display':'inline-block','verticalAlign':'top',
                        'color':'white','margin':'auto'}),



                dcc.Graph(id='my_graph10',
                                figure={'data':[{'x':[1,2],'y':[3,1]}
                                ],
                                'layout':{
                                'plot_bgcolor': colors['light blue'],
                                'paper_bgcolor': colors['light blue'],
                                'height': 260,
                                },}),

                ],className="six columns",style={'display':'inline-block',
                        'width':'33%','padding': 5}),








#=========================================================================================================
                    ], className="row"),
                    html.H2("This price indications are only advisory and may not be accurate"),
                ],style={'backgroundColor': colors['background'],'padding': 25})


#content of tab2


#-------------------------------------------------------------------
#this function will update the current price in the dashboard by collecting live data from various Api
#setting up call backs for input,output and events
@app.callback(Output('my_graph1', 'figure'),
              [Input(component_id='select_financial_asset', component_property='value')],
              events=[Event('graph-update1','interval')])
def update_graph_currentprice(select_financial_asset):
    return update_asset_price.update_price(select_financial_asset)

#------------------------------------------------------------------------------
#this will update the twitter sentiment of selcted asset
@app.callback(Output('my_graph2', 'figure'),
              [Input(component_id='select_financial_asset', component_property='value')],
              events=[Event('graph-update2', 'interval')])
def update_graph_sentiment(select_financial_asset):
    return update_current_sentiment.update_sentiment(select_financial_asset)


#this will update the long term twitter emotion chart
@app.callback(Output('my_graph3', 'figure'),
              [Input(component_id='select_financial_asset', component_property='value')],
              events=[Event('graph-update4', 'interval')])
def update_graph_long_term_emotion(select_financial_asset):
    return update_long_term_sentiment.update_sentiment(select_financial_asset)


#-------------------------------------------------------------------------------
#this will update the pie chart
@app.callback(Output('pie_chart', 'figure'),
              [Input(component_id='select_financial_asset', component_property='value')],
              events=[Event('graph-update4', 'interval')])
def update_pie_chart(select_financial_asset):
    #import update_pichart
    return update_piechart.update(select_financial_asset)


#-------------------------------------------------------------------------------
#this part of the code will update the table with live twee streams

@app.callback(Output('my-table','figure'),
             [Input(component_id='select_financial_asset', component_property='value')],
             events=[Event('graph-update5', 'interval')])
def tweet_table_update(select_financial_asset):
    return update_tweet_table.update_table(select_financial_asset)


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

#============================================================================================
#this will update the price prediction of selected asset
@app.callback(Output('my_graph10', 'figure'),
                 [Input('submit-button1', 'n_clicks')],
                 [State('select_financial_asset_history1', 'value')]
              #events=[Event('graph-update6', 'interval')]
              )
def update_history_graph(n_clicks,select_financial_asset_history1):
    return update_price_prediction_3.update(n_clicks,select_financial_asset_history1)




#-------------------------------------------------------------------------------
#this will update the price prediction pie chart
@app.callback(Output('pie_chart1', 'figure'),
              [Input(component_id='select_financial_asset1', component_property='value')],
              events=[Event('graph-update7', 'interval')])
def update_pie_chart(select_financial_asset1):
    #import update_pichart
    return update_price_prediction_1.update(select_financial_asset1)

#this will update the price prediction  graph 2
@app.callback(Output('pie_chart2', 'figure'),
              [Input(component_id='select_financial_asset1', component_property='value')],
              events=[Event('graph-update8', 'interval')])
def update_pie_chart(select_financial_asset1):
    #import update_pichart
    return update_price_prediction_2.update(select_financial_asset1)

#to populate the price database
@app.callback(Output('label1', 'children'),
            [Input('interval1', 'n_intervals')],)
def update_price_database(n):
     return update_asset_price.populate_table()
    #return update_price_prediction_3.populate_table()


#external css
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
