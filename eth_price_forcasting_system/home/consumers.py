import json
from asyncio import sleep
from unittest import result
from channels.generic.websocket import AsyncWebsocketConsumer
import requests
import pickle
import numpy as np
from tensorflow.keras.models import load_model

def get_predict(input_list, scaler, model, step):
    value_list = input_list
    result_list = []
    

    vector = scaler.transform(np.array(value_list[-19:]).reshape(-1,1))
    vector = np.array(vector).reshape(1,19,1)
    reee = scaler.inverse_transform(model.predict(vector))[0][0]
    print(value_list[-1])
    print(reee)
    rate_value = int(float(value_list[-1]))-int(float(reee))
    for i in range(step):
        vector = scaler.transform(np.array(value_list[-19:]).reshape(-1,1))
        vector = np.array(vector).reshape(1,19,1)
        reee = scaler.inverse_transform(model.predict(vector))[0][0]
        result_list.append(reee+rate_value)
        value_list.append(reee+rate_value)
        print(value_list[-19:])
    return result_list

scaler = pickle.load(open('ml_model/lstm_scaler.sav', 'rb'))

lstm_model_19Sstep = load_model('ml_model/eth_price_LSTM_model_v16_19Sstep.h5')

s_step_value = []

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
       
        while True:
            
            if len(s_step_value)<19:
                x = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
                print(x.json()["data"]["amount"])
                s_step_value.append(x.json()["data"]["amount"])
                await self.send(json.dumps({'value':x.json()["data"]["amount"],
                                            'predict':x.json()["data"]["amount"],
                                            }))
                await sleep(1)
            
            else:
                x = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
                
                result = self.get_vector()

                s_step_value.append(x.json()["data"]["amount"])
                
                await self.send(json.dumps({'value':x.json()["data"]["amount"],
                                            'predict0':result[0],
                                            'predict1':result[1],
                                            'predict2':result[2],
                                            'predict3':result[3],
                                            'predict4':result[4],
                                        }))
                await sleep(1)
    
    # def get_vector(self):
    #     vector = scaler.transform(np.array(s_step_value[-19:]).reshape(-1,1))
    #     vector = np.array(vector).reshape(1,19,1)
    #     predict = lstm_model_19Sstep.predict(vector)
    #     result = scaler.inverse_transform(predict)[0][1]
    #     print('-'*10)
    #     print(result)
    #     print('-'*10)
    #     return float(result+200)

    def get_vector(self):
        result_list = get_predict(s_step_value[-19:], scaler, lstm_model_19Sstep, 5)
        return result_list