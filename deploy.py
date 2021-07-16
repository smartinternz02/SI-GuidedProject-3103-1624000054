# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 18:57:25 2021

@author: pavan kalyan
"""
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "gKYEpP7dSPMk9htn58RQUxRT-NDamWJidwl5Fo8d8Vr9"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"field": [["Current Loan Amount","Term","Credit Score","Annual Income","Years in current job","Home Ownership","Years of Credit History","Number of Credit Problems","Bankruptcies","Tax Liens","Credit Problems","Credit Age"]], "values": [[445412.0,0,709.0,1167493.0	,8,"1",17.2	,1.0,1.0,0.0,1,5]]}]}

import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
import os

app = Flask(__name__)
model = pickle.load(open('loan.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('LoanStatus.html')


@app.route('/predict', methods=['POST'])
def predict():
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]

    features_name = ['Current Loan Amount', 'Term', 'Credit Score', 'Annual Income',
                     'Years in current job', 'Home Ownership', 'Years of Credit History',
                     'Number of Credit Problems', 'Bankruptcies', 'Tax Liens',
                     'Credit Problems', 'Credit Age']

    #df = pd.DataFrame(features_value, columns=features_name)
    #output = model.predict(df)
    #if output == 1:
     #   return render_template('FullyPaid.html')
    #else:
     #   return render_template('Charged.html')

    payload_scoring = {"input_data": [{"field": [["Current Loan Amount","Term","Credit Score","Annual Income","Years in current job","Home Ownership","Years of Credit History","Number of Credit Problems","Bankruptcies","Tax Liens","Credit Problems","Credit Age"]], "values": [[input_features[0],input_features[1],input_features[2],input_features[3],input_features[4],input_features[5],input_features[6],input_features[7],input_features[8],input_features[9],input_features[10],input_features[11]]]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b5cb86de-12ec-451c-a666-7ff461cff878/predictions?version=2021-07-06', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions=response_scoring.json()
    result = predictions['predictions'][0]['values'][0][0]
    if(result==0):
        return render_template('ChargedOff.html')
    else:
        return render_template('FullyPaid.html')
if __name__ == '__main__':
    #app.run(debug=True)
    app.run('127.0.0.1', 5000)