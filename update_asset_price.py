import sqlite3
import pandas as pd
import json
import forex_python
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
import time
import datetime
import plotly.graph_objs as go



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
#--------------------------------
time_list=[]
#this list will hold the price of bitcoin
b_price_list = []
#this list will hold the price of dollar
d_price_list=[]
#this list will hold the price of pound
p_price_list=[]
#this list will hold the price of euro
e_price_list=[]
#this list will hold the price of yen
y_price_list=[]

def create_table():
    conn1 = sqlite3.connect('asset_prices.db')
    c1 = conn1.cursor()
    try:
        c1.execute("CREATE TABLE IF NOT EXISTS PRICES(Bitcoin_value REAL,Dollar_value REAL,Pound_value REAL,Yen_value REAL,Euro_value REAL)")
        conn1.commit()
    except Exception as e:
        print(str(e))
#calling creat table () function
create_table()
#creating bitcoin currency convertor

#creating sql database for asset prices
def populate_table():
        conn1 = sqlite3.connect('asset_prices.db')
        c1 = conn1.cursor()
        cur1 = CurrencyRates()
        cur2 = CurrencyRates()
        dollar=cur1.get_rate('USD', 'GBP')
        pound=cur2.get_rate( 'GBP','USD')
        yen=cur1.get_rate('JPY','USD')
        euro=cur2.get_rate('EUR','USD')


        b = BtcConverter()
            #getting the live updated price of bitcoin from forex python api
        bp=b.get_latest_price('USD')
        v=bp
        #print(bp)
        #print("===============")
        c1.execute("INSERT INTO  PRICES(Bitcoin_value,Dollar_value,Pound_value,Yen_value,Euro_value) VALUES (?,?,?,?,?)",
        (bp,dollar,pound,yen,euro,))
        conn1.commit()


#==========================================

def update_price(select_financial_asset):
    if select_financial_asset == 'Bitcoin':
        #========================================

        #creating table

        #creating currency convertor
        #c = CurrencyRates()
        #creating bitcoin currency convertor
        b = BtcConverter()
        #getting the live updated price of bitcoin from forex python api
        bp=b.get_latest_price('USD')



        #currenttime=time.asctime(time.localtime(time.time()))
        #obtaining the current time and conduct formatting
        currenttime = datetime.datetime.now()
        time=currenttime.strftime("%Y-%m-%d %H:%M:%S")
        #print(bp)
        #adding current time to the time list
        time_list.append(time)
        #adding bitcoing price to the list as soon as collected from api
        b_price_list.append(bp)
        data = go.Scatter(
                x=time_list,
                #x = list(range(len(time_list))),
                y = b_price_list,
                name='Scatter',
                mode= 'lines+markers',
                fillcolor=colors['blue'],
                marker = dict( size = 2,color = colors['light blue'],
                        line = dict(width = 2,)))
        return {'data': [data],'layout' : go.Layout(
                        width=450,
                        #width=695,
                        height=300,
                        margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=5),
                        autosize=False,
                        xaxis=dict(title='Time'),
                        yaxis=dict(title='Price in USD'),
                        hovermode='closest',

                        font=dict(family='Courier New, monospace', size=11, color='blue'),

                        #plot_bgcolor=colors['background'],
                        title=('current price of '+select_financial_asset+
                        ' is :'+str(bp))+' USD'),

                        }

    elif select_financial_asset == 'Dollar':
        #this api have limited amount of request allowance.can get more with subscription
        '''
        #send the request for the price
        url = 'https://v3.exchangerate-api.com/pair/dbecbd8f5e863e0ad72cd94b/USD/GBP'
        #collecting the response and put it into json
        response = requests.get(url)
        data = response.json()
        #taking just the current rate from json data
        f= (data['rate'])
        '''
        #this api dones not update the price frequently but free to use
        c = CurrencyRates()
        f=c.get_rate('USD', 'GBP')
        #obtaining the current time and conduct formatting
        currenttime = datetime.datetime.now()
        time=currenttime.strftime("%Y-%m-%d %H:%M:%S")
        #adding current time to the time list
        time_list.append(time)
        #adding dollar price to the list as soon as collected from api
        d_price_list.append(f)
        data = go.Scatter(
                x=time_list,
                y = d_price_list,
                name='Scatter',
                mode= 'lines+markers',
                fillcolor=colors['blue'],
                marker = dict(  size = 2,color = colors['light blue'],
                        line = dict(width = 2,)))
        return {'data': [data],'layout' : go.Layout(
                        xaxis=dict(title='Time'),
                        yaxis=dict(title='Price in GBP'),
                        hovermode='closest',
                        margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=5),
                        #plot_bgcolor=colors['background'],
                        font=dict(family='Courier New, monospace', size=11, color='blue'),
                        title=('current price of '+select_financial_asset+
                        ' is :'+str(f))+' GBP')}
    elif select_financial_asset == 'Pound':
        #this api have limited amount of request allowance.can get more with subscription
        '''
        #send the request for the price
        url = 'https://v3.exchangerate-api.com/pair/dbecbd8f5e863e0ad72cd94b/GBP/USD'
        #collecting the response and put it into json
        response = requests.get(url)
        data = response.json()
        #taking just the current rate from json data
        f= (data['rate'])
        '''
        #this api dones not update the price frequently but free to use
        c = CurrencyRates()
        f=c.get_rate( 'GBP','USD')
        #obtaining the current time and conduct formatting
        currenttime = datetime.datetime.now()
        time=currenttime.strftime("%Y-%m-%d %H:%M:%S")
        #adding current time to the time list
        time_list.append(time)
        #adding pound price to the list as soon as collected from api
        p_price_list.append(f)
        data = go.Scatter(
                x=time_list,
                #x = list(range(len(time_list))),
                y = p_price_list,
                name='Scatter',
                mode= 'lines+markers',
                fillcolor=colors['blue'],
                marker = dict(size = 2,color = colors['light blue'],
                        line = dict(width = 2,)))
        return {'data': [data],'layout' : go.Layout(
                        xaxis=dict(title='Time'),
                        yaxis=dict(title='Price in USD'),
                        hovermode='closest',
                        margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=5),
                        #plot_bgcolor=colors['background'],
                        font=dict(family='Courier New, monospace', size=11, color='blue'),
                        title=('current price of '+select_financial_asset+
                        ' is :'+str(f))+' USD')}
    elif select_financial_asset == 'Euro':
        #this api have limited amount of request allowance.can get more with subscription
        '''
        #send the request for the price
        url = 'https://v3.exchangerate-api.com/pair/dbecbd8f5e863e0ad72cd94b/EUR/USD'
        #collecting the response and put it into json
        response = requests.get(url)
        data = response.json()
        #taking just the current rate from json data
        f= (data['rate'])
        '''
        #this api dones not update the price frequently but free to use
        c = CurrencyRates()
        f=c.get_rate('EUR','USD')
        #obtaining the current time and conduct formatting
        currenttime = datetime.datetime.now()
        time=currenttime.strftime("%Y-%m-%d %H:%M:%S")
        #adding current time to the time list
        time_list.append(time)
        #adding euro price to the list as soon as collected from api
        e_price_list.append(f)
        data = go.Scatter(
                x=time_list,
                y = e_price_list,
                name='Scatter',
                mode= 'lines+markers',
                fillcolor=colors['blue'],
                marker = dict( size = 2,color = colors['light blue'],
                        line = dict(width = 2,)))
        return {'data': [data],'layout' : go.Layout(
                        xaxis=dict(title='Time'),
                        yaxis=dict(title='Price in USD'),
                        hovermode='closest',
                        margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=5),

                        #plot_bgcolor=colors['background'],
                        font=dict(family='Courier New, monospace', size=11, color='blue'),
                        title=('current price of '+select_financial_asset+
                        ' is :'+str(f))+' USD')}

    elif select_financial_asset == 'Yen':
        #this api have limited amount of request allowance.can get more with subscription
        '''
        #send the request for the price
        url = 'https://v3.exchangerate-api.com/pair/dbecbd8f5e863e0ad72cd94b/JPY/USD'
        #collecting the response and put it into json
        response = requests.get(url)
        data = response.json()
        #taking just the current rate from json data
        f= (data['rate'])
        '''
        #this api dones not update the price frequently but free to use
        c = CurrencyRates()
        f=c.get_rate('JPY','USD')
        #obtaining the current time and conduct formatting
        currenttime = datetime.datetime.now()
        time=currenttime.strftime("%Y-%m-%d %H:%M:%S")
        #adding current time to the time list
        time_list.append(time)
        #adding yen price to the list as soon as collected from api
        y_price_list.append(f)
        data = go.Scatter(
                x=time_list,
                y = y_price_list,
                name='Scatter',
                mode= 'lines+markers',
                fillcolor=colors['blue'],
                marker = dict( size = 2,color = colors['light blue'],
                        line = dict(width = 2,)))
        return {'data': [data],'layout' : go.Layout(
                        xaxis=dict(title='Time'),
                        yaxis=dict(title='Price in USD'),
                        hovermode='closest',
                        margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=5),
                        #plot_bgcolor=colors['background'],
                        font=dict(family='Courier New, monospace', size=11, color='blue'),
                        title=('current price of '+select_financial_asset+
                        ' is :'+str(f))+' USD')}

    else:
        print('Erorr!!!')
