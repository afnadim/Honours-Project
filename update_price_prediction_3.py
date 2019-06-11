import sqlite3
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

from sklearn.preprocessing import MinMaxScaler
min_max_scaler = MinMaxScaler()

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

def update(n_clicks,select_financial_asset_history1):
    if select_financial_asset_history1 == 'Bitcoin':
    #bitcoin='Bitcoin'# Create a Dash layout that contains a Graph component:
    #taking in the datasetr
        conn = sqlite3.connect('asset_prices.db')
        c = conn.cursor()
        #df = pd.read_sql("SELECT * FROM PRICES WHERE Bitcoin_value LIKE ? LIMIT 100", conn ,params=('%' + select_financial_asset_history1 + '%',))
        df = pd.read_sql("select Bitcoin_value FROM PRICES limit 1000;",conn)
        #split the dataset into trainning and testing
        days=[0,1,2,3,4,5,6,7,8,9]
        prediction_days = 10
        df_train= df[:len(df)-prediction_days]
        df_test= df[len(df)-prediction_days:]
        
        #normalise and prepare for testing
        training_set = df_train.values
        training_set = min_max_scaler.fit_transform(training_set)

        x_train = training_set[0:len(training_set)-1]
        y_train = training_set[1:len(training_set)]
        x_train = np.reshape(x_train, (len(x_train), 1, 1))



        #trainning the model
        num_units = 4
        activation_function = 'sigmoid'
        optimizer = 'adam'
        loss_function = 'mean_squared_error'
        batch_size = 5
        num_epochs = 10

        # Initialize the RNN
        regressor = Sequential()
        # Adding the input layer and the LSTM layer
        regressor.add(LSTM(units = num_units, activation = activation_function, input_shape=(None, 1)))
        # Adding the output layer
        regressor.add(Dense(units = 1))
        # Compiling the RNN
        regressor.compile(optimizer = optimizer, loss = loss_function)
        # Using the training set to train the model
        regressor.fit(x_train, y_train, batch_size = batch_size, epochs = num_epochs)


        #predict the BitcoinPrice

        test_set = df_test.values

        inputs = np.reshape(test_set, (len(test_set), 1))
        inputs = min_max_scaler.transform(inputs)
        inputs = np.reshape(inputs, (len(inputs), 1, 1))

        predicted_price = regressor.predict(inputs)
        predicted_price = min_max_scaler.inverse_transform(predicted_price)

        labels = ['Price']
        df1 = pd.DataFrame.from_records(predicted_price, columns=labels)
        #print(df1.head)

        Y = df1.Price.values[:9]
        X = df1.index.values[:9]

        #print(predicted_price)
        data = go.Scatter(
                x=X,
                y = Y,
                name='Scatter',
                mode= 'lines+markers',
                fillcolor=colors['blue'],
                marker = dict( size = 2,color = colors['light blue'],
                        line = dict(width = 2,)))
        return {'data': [data],'layout' : go.Layout(
                        xaxis=dict(title='days'),
                        yaxis=dict(title='Price in USD'),
                        hovermode='closest',
                        margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=0),
                        #plot_bgcolor=colors['background'],
                        font=dict(family='Courier New, monospace', size=11, color='blue'),
                        title=('price prediction of : '+select_financial_asset_history1)



                        )}


#====================================================================
    elif select_financial_asset_history1 == 'Dollar':
            #taking in the datasetr
                conn = sqlite3.connect('asset_prices.db')
                c = conn.cursor()
                #df = pd.read_sql("SELECT * FROM PRICES WHERE Bitcoin_value LIKE ? LIMIT 100", conn ,params=('%' + select_financial_asset_history1 + '%',))
                df = pd.read_sql("select Dollar_value FROM PRICES limit 1000;",conn)

                #df.sort_values('unix', inplace=True)
                #df.to_csv('out.csv')

                #df = pd.read_csv('BitcoinPrice.csv')
                #df= df.drop(df.columns[0], axis=1)

                #print(df_norm.shape)

                #split the dataset into trainning and testing
                days=[0,1,2,3,4,5,6,7,8,9]
                prediction_days = 10

                df_train= df[:len(df)-prediction_days]
                df_test= df[len(df)-prediction_days:]
                #print(df_train.head)

                #print("i am here after train and test split")

                #normalise and prepare for testing
                training_set = df_train.values
                training_set = min_max_scaler.fit_transform(training_set)

                x_train = training_set[0:len(training_set)-1]
                y_train = training_set[1:len(training_set)]
                x_train = np.reshape(x_train, (len(x_train), 1, 1))

            #    print("i am here after----preparation for testing")

                #trainning the model

                num_units = 4
                activation_function = 'sigmoid'
                optimizer = 'adam'
                loss_function = 'mean_squared_error'
                batch_size = 5
                num_epochs = 10

                # Initialize the RNN
                regressor = Sequential()

                # Adding the input layer and the LSTM layer
                regressor.add(LSTM(units = num_units, activation = activation_function, input_shape=(None, 1)))

                # Adding the output layer
                regressor.add(Dense(units = 1))

                # Compiling the RNN
                regressor.compile(optimizer = optimizer, loss = loss_function)

                # Using the training set to train the model
                regressor.fit(x_train, y_train, batch_size = batch_size, epochs = num_epochs)

                #print("i am here after----trainning the model")

                #predict the BitcoinPrice

                test_set = df_test.values

                inputs = np.reshape(test_set, (len(test_set), 1))
                inputs = min_max_scaler.transform(inputs)
                inputs = np.reshape(inputs, (len(inputs), 1, 1))

                predicted_price = regressor.predict(inputs)
                predicted_price = min_max_scaler.inverse_transform(predicted_price)

                labels = ['Price']
                df1 = pd.DataFrame.from_records(predicted_price, columns=labels)
                #print(df1.head)

                Y = df1.Price.values[:9]
                X = df1.index.values[:9]

                #print(predicted_price)
                data = go.Scatter(
                        x=X,
                        y = Y,
                        name='Scatter',
                        mode= 'lines+markers',
                        fillcolor=colors['blue'],
                        marker = dict( size = 2,color = colors['light blue'],
                                line = dict(width = 2,)))
                return {'data': [data],'layout' : go.Layout(
                                xaxis=dict(title='days'),
                                yaxis=dict(title='Price in USD'),
                                hovermode='closest',
                                margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=0),
                                #plot_bgcolor=colors['background'],
                                font=dict(family='Courier New, monospace', size=11, color='blue'),
                                title=('price prediction of : '+select_financial_asset_history1)
                                )}

#===========================================================================
    elif select_financial_asset_history1 == 'Euro':
            #taking in the datasetr
                conn = sqlite3.connect('asset_prices.db')
                c = conn.cursor()
                #df = pd.read_sql("SELECT * FROM PRICES WHERE Bitcoin_value LIKE ? LIMIT 100", conn ,params=('%' + select_financial_asset_history1 + '%',))
                df = pd.read_sql("select Euro_value FROM PRICES limit 1000;",conn)

                #df.sort_values('unix', inplace=True)
                #df.to_csv('out.csv')

                #df = pd.read_csv('BitcoinPrice.csv')
                #df= df.drop(df.columns[0], axis=1)

                #print(df_norm.shape)

                #split the dataset into trainning and testing
                days=[0,1,2,3,4,5,6,7,8,9]
                prediction_days = 10

                df_train= df[:len(df)-prediction_days]
                df_test= df[len(df)-prediction_days:]
                #print(df_train.head)

                #print("i am here after train and test split")

                #normalise and prepare for testing
                training_set = df_train.values
                training_set = min_max_scaler.fit_transform(training_set)

                x_train = training_set[0:len(training_set)-1]
                y_train = training_set[1:len(training_set)]
                x_train = np.reshape(x_train, (len(x_train), 1, 1))

                #print("i am here after----preparation for testing")

                #trainning the model

                num_units = 4
                activation_function = 'sigmoid'
                optimizer = 'adam'
                loss_function = 'mean_squared_error'
                batch_size = 5
                num_epochs = 10

                # Initialize the RNN
                regressor = Sequential()

                # Adding the input layer and the LSTM layer
                regressor.add(LSTM(units = num_units, activation = activation_function, input_shape=(None, 1)))

                # Adding the output layer
                regressor.add(Dense(units = 1))

                # Compiling the RNN
                regressor.compile(optimizer = optimizer, loss = loss_function)

                # Using the training set to train the model
                regressor.fit(x_train, y_train, batch_size = batch_size, epochs = num_epochs)

                #print("i am here after----trainning the model")

                #predict the BitcoinPrice

                test_set = df_test.values

                inputs = np.reshape(test_set, (len(test_set), 1))
                inputs = min_max_scaler.transform(inputs)
                inputs = np.reshape(inputs, (len(inputs), 1, 1))

                predicted_price = regressor.predict(inputs)
                predicted_price = min_max_scaler.inverse_transform(predicted_price)

                labels = ['Price']
                df1 = pd.DataFrame.from_records(predicted_price, columns=labels)
                #print(df1.head)

                Y = df1.Price.values[:9]
                X = df1.index.values[:9]

                #print(predicted_price)
                data = go.Scatter(
                        x=X,
                        y = Y,
                        name='Scatter',
                        mode= 'lines+markers',
                        fillcolor=colors['blue'],
                        marker = dict( size = 2,color = colors['light blue'],
                                line = dict(width = 2,)))
                return {'data': [data],'layout' : go.Layout(
                                xaxis=dict(title='days'),
                                yaxis=dict(title='Price in USD'),
                                hovermode='closest',
                                margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=0),
                                #plot_bgcolor=colors['background'],
                                font=dict(family='Courier New, monospace', size=11, color='blue'),
                                title=('price prediction of : '+select_financial_asset_history1)
                                )}


#===========================================================================
    elif select_financial_asset_history1 == 'Pound':
            #taking in the datasetr
                conn = sqlite3.connect('asset_prices.db')
                c = conn.cursor()
                #df = pd.read_sql("SELECT * FROM PRICES WHERE Bitcoin_value LIKE ? LIMIT 100", conn ,params=('%' + select_financial_asset_history1 + '%',))
                df = pd.read_sql("select Pound_value FROM PRICES limit 1000;",conn)

                #df.sort_values('unix', inplace=True)
                #df.to_csv('out.csv')

                #df = pd.read_csv('BitcoinPrice.csv')
                #df= df.drop(df.columns[0], axis=1)

                #print(df_norm.shape)

                #split the dataset into trainning and testing
                days=[0,1,2,3,4,5,6,7,8,9]
                prediction_days = 10

                df_train= df[:len(df)-prediction_days]
                df_test= df[len(df)-prediction_days:]
                #print(df_train.head)

                #print("i am here after train and test split")

                #normalise and prepare for testing
                training_set = df_train.values
                training_set = min_max_scaler.fit_transform(training_set)

                x_train = training_set[0:len(training_set)-1]
                y_train = training_set[1:len(training_set)]
                x_train = np.reshape(x_train, (len(x_train), 1, 1))

                #print("i am here after----preparation for testing")

                #trainning the model

                num_units = 4
                activation_function = 'sigmoid'
                optimizer = 'adam'
                loss_function = 'mean_squared_error'
                batch_size = 5
                num_epochs = 10

                # Initialize the RNN
                regressor = Sequential()

                # Adding the input layer and the LSTM layer
                regressor.add(LSTM(units = num_units, activation = activation_function, input_shape=(None, 1)))

                # Adding the output layer
                regressor.add(Dense(units = 1))

                # Compiling the RNN
                regressor.compile(optimizer = optimizer, loss = loss_function)

                # Using the training set to train the model
                regressor.fit(x_train, y_train, batch_size = batch_size, epochs = num_epochs)

                #print("i am here after----trainning the model")

                #predict the BitcoinPrice

                test_set = df_test.values

                inputs = np.reshape(test_set, (len(test_set), 1))
                inputs = min_max_scaler.transform(inputs)
                inputs = np.reshape(inputs, (len(inputs), 1, 1))

                predicted_price = regressor.predict(inputs)
                predicted_price = min_max_scaler.inverse_transform(predicted_price)

                labels = ['Price']
                df1 = pd.DataFrame.from_records(predicted_price, columns=labels)
                #print(df1.head)

                Y = df1.Price.values[:9]
                X = df1.index.values[:9]

                #print(predicted_price)
                data = go.Scatter(
                        x=X,
                        y = Y,
                        name='Scatter',
                        mode= 'lines+markers',
                        fillcolor=colors['blue'],
                        marker = dict( size = 2,color = colors['light blue'],
                                line = dict(width = 2,)))
                return {'data': [data],'layout' : go.Layout(
                                xaxis=dict(title='days'),
                                yaxis=dict(title='Price in USD'),
                                hovermode='closest',
                                margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=0),
                                #plot_bgcolor=colors['background'],
                                font=dict(family='Courier New, monospace', size=11, color='blue'),
                                title=('price prediction of : '+select_financial_asset_history1)
                                )}


#===========================================================================
    elif select_financial_asset_history1 == 'Yen':
            #taking in the datasetr
                conn = sqlite3.connect('asset_prices.db')
                c = conn.cursor()
                #df = pd.read_sql("SELECT * FROM PRICES WHERE Bitcoin_value LIKE ? LIMIT 100", conn ,params=('%' + select_financial_asset_history1 + '%',))
                df = pd.read_sql("select Yen_value FROM PRICES limit 1000;",conn)

                #df.sort_values('unix', inplace=True)
                #df.to_csv('out.csv')

                #df = pd.read_csv('BitcoinPrice.csv')
                #df= df.drop(df.columns[0], axis=1)

                #print(df_norm.shape)

                #split the dataset into trainning and testing
                days=[0,1,2,3,4,5,6,7,8,9]
                prediction_days = 10

                df_train= df[:len(df)-prediction_days]
                df_test= df[len(df)-prediction_days:]
                #print(df_train.head)

                #print("i am here after train and test split")

                #normalise and prepare for testing
                training_set = df_train.values
                training_set = min_max_scaler.fit_transform(training_set)

                x_train = training_set[0:len(training_set)-1]
                y_train = training_set[1:len(training_set)]
                x_train = np.reshape(x_train, (len(x_train), 1, 1))

                #print("i am here after----preparation for testing")

                #trainning the model

                num_units = 4
                activation_function = 'sigmoid'
                optimizer = 'adam'
                loss_function = 'mean_squared_error'
                batch_size = 5
                num_epochs = 10

                # Initialize the RNN
                regressor = Sequential()

                # Adding the input layer and the LSTM layer
                regressor.add(LSTM(units = num_units, activation = activation_function, input_shape=(None, 1)))

                # Adding the output layer
                regressor.add(Dense(units = 1))

                # Compiling the RNN
                regressor.compile(optimizer = optimizer, loss = loss_function)

                # Using the training set to train the model
                regressor.fit(x_train, y_train, batch_size = batch_size, epochs = num_epochs)

                #print("i am here after----trainning the model")

                #predict the BitcoinPrice

                test_set = df_test.values

                inputs = np.reshape(test_set, (len(test_set), 1))
                inputs = min_max_scaler.transform(inputs)
                inputs = np.reshape(inputs, (len(inputs), 1, 1))

                predicted_price = regressor.predict(inputs)
                predicted_price = min_max_scaler.inverse_transform(predicted_price)

                labels = ['Price']
                df1 = pd.DataFrame.from_records(predicted_price, columns=labels)
                #print(df1.head)

                Y = df1.Price.values[:9]
                X = df1.index.values[:9]

                #print(predicted_price)
                data = go.Scatter(
                        x=X,
                        y = Y,
                        name='Scatter',
                        mode= 'lines+markers',
                        fillcolor=colors['blue'],
                        marker = dict( size = 2,color = colors['light blue'],
                                line = dict(width = 2,)))
                return {'data': [data],'layout' : go.Layout(
                                xaxis=dict(title='days'),
                                yaxis=dict(title='Price in USD'),
                                hovermode='closest',
                                margin=go.layout.Margin(l=30,r=30,b=50,t=70,pad=0),
                                #plot_bgcolor=colors['background'],
                                font=dict(family='Courier New, monospace', size=11, color='blue'),
                                title=('price prediction of : '+select_financial_asset_history1)
                                )}
