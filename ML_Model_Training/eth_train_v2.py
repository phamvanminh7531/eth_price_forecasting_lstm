# Develop by PVM - Steam - K22 - FIRA

# Training with realtime datatset (Time Series 2 seconds step)

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import LSTM
import glob

list_of_files = glob.glob('./dataset/*.csv')

frames = []
for i in list_of_files:
    df = pd.read_csv(i)
    df.columns = ["time","value"]
    frames.append(df)
data = pd.concat(frames)
print(data.info())
price_value = data["value"]

price_value_list = []
for i in price_value:
    price_value_list.append(i)

scaler = MinMaxScaler()
close_price = np.array(price_value_list).reshape(-1,1)
b = np.array([0,3000]).reshape(-1,1)
c = np.concatenate((b,close_price))
scaler.fit(c)
scaled_close = scaler.transform(close_price)


SEQ_LEN = 20

def to_sequences(data, seq_len):
    d = []

    for index in range(len(data) - seq_len):
        d.append(data[index: index + seq_len])

    return np.array(d)

def preprocess(data_raw, seq_len, train_split):

    data = to_sequences(data_raw, seq_len)

    num_train = int(train_split * data.shape[0])

    X_train = data[:num_train, :-1, :]
    y_train = data[:num_train, -1, :]

    X_test = data[num_train:, :-1, :]
    y_test = data[num_train:, -1, :]

    return X_train, y_train, X_test, y_test


X_train, y_train, X_test, y_test = preprocess(scaled_close, SEQ_LEN, train_split = 0.90)

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape = (X_train.shape[1], X_train.shape[2])))

model.add(Dropout(0.1)) 
model.add(LSTM(units=50))

model.add(Dense(2))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_absolute_error'])

model.summary()

model.fit(X_train, y_train,batch_size=2048, epochs=100,validation_data=(X_test, y_test), verbose=1)

model.save('eth_price_LSTM_model_v16_19Sstep.h5')




