#Develop by PVM - Steam - K22 - FIRA


from django.shortcuts import render
import requests
import pickle
from tensorflow.keras.models import load_model
import numpy as np
from datetime import date, datetime
from bs4 import BeautifulSoup

def get_predict(input_list, scaler, model):
    value_list = input_list
    result_list = []
    

    vector = scaler.transform(np.array(value_list[-19:]).reshape(-1,1))
    vector = np.array(vector).reshape(1,19,1)
    reee = scaler.inverse_transform(model.predict(vector))[0][0]
    rate_value = value_list[-1]-reee
    for i in range(5):
        vector = scaler.transform(np.array(value_list[-19:]).reshape(-1,1))
        vector = np.array(vector).reshape(1,19,1)
        reee = scaler.inverse_transform(model.predict(vector))[0][0]
        result_list.append(reee+rate_value)
        value_list.append(reee+rate_value)
        print(value_list[-19:])
    return result_list

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def warning(request):
    return render(request, 'home/warning.html')

def daily(request):
    scaler = pickle.load(open('ml_model/lstm_scaler.sav', 'rb'))
    lstm = load_model('ml_model/eth_price_LSTM_model_v16_19Sstep.h5')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    url = 'https://finance.yahoo.com/quote/ETH-USD/history/'
    r = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    _value_list = []
    input_list = []

    rows = soup.findAll('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)')
    for row in rows[:19]:
        _value_list.append(float(str(row).split('<span>')[2].split('</span>')[0].replace(',','')))
        input_list.append(float(str(row).split('<span>')[2].split('</span>')[0].replace(',','')))
    
    _value_list.reverse()
    input_list.reverse()

  
    print(len(_value_list))
    result_list = get_predict(input_list, scaler, lstm)

    print('-'*20)
    print(len(_value_list))
    print('-'*20)
    print(len(result_list))
    print('-'*20)
    context = {
        "value":_value_list,
        "future":_value_list+result_list
    }
    return render(request, 'home/daily.html', context)
    
