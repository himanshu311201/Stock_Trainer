def lstm_prediction(se, stock_symbol):
    import pandas as pd
    import numpy as np
    from tensorflow.keras.models import load_model

    def fetch_stock_data(se, stock_symbol):
        """fetch stock data"""
        from pandas_datareader import data as pdr
        import yfinance as yf
        yf.pdr_override()
        if se == 'NSE':
            stock_symbol += ".NS"
        return pdr.get_data_yahoo(stock_symbol, period="5y")

    """LSTM model development"""
    from sklearn.preprocessing import MinMaxScaler
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, LSTM

    og_df = fetch_stock_data(se, stock_symbol)
    todataframe = og_df.reset_index(inplace=False)

    # dataframe creation
    seriesdata = todataframe.sort_index(ascending=True, axis=0)
    new_seriesdata = pd.DataFrame(index=range(0, len(todataframe)), columns=['Date', 'Close'])
    for i in range(0, len(seriesdata)):
        new_seriesdata['Date'][i] = seriesdata['Date'][i]
        new_seriesdata['Close'][i] = seriesdata['Close'][i]
    # setting the index again
    new_seriesdata.index = new_seriesdata.Date
    new_seriesdata.drop('Date', axis=1, inplace=True)

    import os
    x = '../Stock_Trainer/Stock_Game/static/Stock_Game/data/'
    y = stock_symbol
    z = '.h5'

    print(x+y+z, os.path.exists(x+y+z))

    if(os.path.exists(x+y+z)):
        model = load_model(x+y+z)
    else:
        # creating train and test sets this comprises the entire data’s present in the dataset
        myseriesdataset = new_seriesdata.values
        totrain = myseriesdataset
        # converting dataset into x_train and y_train
        scalerdata = MinMaxScaler(feature_range=(0, 1))
        scale_data = scalerdata.fit_transform(myseriesdataset)
        x_totrain, y_totrain = [], []
        length_of_totrain = len(totrain)
        for i in range(100, length_of_totrain):
            x_totrain.append(scale_data[i - 100:i, 0])
            y_totrain.append(scale_data[i, 0])

        x_totrain, y_totrain = np.array(x_totrain), np.array(y_totrain)
        x_totrain = np.reshape(x_totrain, (x_totrain.shape[0], x_totrain.shape[1], 1))

        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Dropout
        from tensorflow.keras.layers import LSTM

        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(x_totrain.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')

        model.summary()

        model.fit(x_totrain, y_totrain, epochs=100, batch_size=64, verbose=1)

        c = '../Stock_Trainer/Stock_Game/static/Stock_Game/data/'
        a = stock_symbol
        b = '.h5'
        model.save(c+a+b)

    close = new_seriesdata["Close"]
    close = close.dropna()
    scaler = MinMaxScaler(feature_range=(0, 1))
    tmp = scaler.fit(np.array(close).reshape(-1, 1))
    new_df = scaler.transform(np.array(close).reshape(-1, 1))

    test_data = close
    test_data = scaler.transform(np.array(close).reshape(-1, 1))
    test_data = test_data.reshape((-1))

    n_steps = 100

    def predict(num_prediction, model):
        prediction_list = test_data[-n_steps:]

        for _ in range(num_prediction):
            x = prediction_list[-n_steps:]
            x = x.reshape((1, n_steps, 1))
            out = model.predict(x)[0][0]
            prediction_list = np.append(prediction_list, out)
        prediction_list = prediction_list[n_steps - 1:]

        return prediction_list

    x = predict(100, model)

    x = x.reshape(1, -1)
    x = scaler.inverse_transform(x)
    myclosing_priceresult = x
    myclosing_priceresult = myclosing_priceresult.reshape(-1, 1)
    myclosing_priceresult
    # import matplotlib.pyplot as plt

    # plt.plot(result_df['Close'])

    # plt.show()

    # Combining og and predicted dataset for end result.
    datelist = pd.date_range(pd.datetime.now().date(), periods=102)[1:]
    predicted_df = pd.DataFrame(myclosing_priceresult, columns=['Close'], index=datelist)
    result_df = pd.concat([og_df, predicted_df])[['Close']]
    result_df = result_df.reset_index(inplace=False)
    result_df.columns = ['Date', 'Close']

    def get_json(df):
        """ Small function to serialise DataFrame dates as 'YYYY-MM-DD' in JSON """
        import json
        import datetime
        def convert_timestamp(item_date_object):
            if isinstance(item_date_object, (datetime.date, datetime.datetime)):
                return item_date_object.strftime("%Y-%m-%d")

        dict_ = df.to_dict(orient='records')

        return json.dumps(dict_, default=convert_timestamp)

    return get_json(result_df)