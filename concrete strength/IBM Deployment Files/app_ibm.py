import numpy as np
from flask import Flask, render_template, request
import pandas as pd

import requests


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account
API_KEY = "SIWh-3Wte2pfbwYHOWKw_VRXA1OdfH7rYkBBI9YEqjnT"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__) # initializing a flask app
#model = pickle.load(open('cement1.pkl', 'rb'))

@app.route('/')# route to display the home page
def home():
    return render_template('home.html') #rendering the home page
@app.route('/Prediction',methods=['POST','GET'])
def prediction():
    return render_template('index1.html')
@app.route('/Home',methods=['POST','GET'])
def my_home():
    return render_template('home.html')
@app.route('/predict',methods=['POST']) # route to show the predictions in a web UI

def index():
            #  reading the inputs given by the user
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    features_name = ['Cement', 'Blast Furnace Slag', 'Fly Ash', 'Water',
                     'Superplasticizer','Coarse Aggregate', 'Fine Aggregate','Age']
    x = pd.DataFrame(features_value, columns=features_name)
    x_log=np.log(features_value)#performing log transformation
    x_log=x_log.tolist()
    # predictions using the loaded model file
    #prediction=model.predict(x_log)
    payload_scoring = {"input_data": [
        {"field": ["cement", "slag", "ash", "Water", "superplastic", "coarseagg", "fineagg", "age"],"values": x_log}]}
    response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e32379f4-c48c-41d1-ad13-eff9b2a4d38e/predictions?version=2022-07-29",json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    pred = response_scoring.json()
    print(pred)
    output = pred['predictions'][0]['values'][0][0]
    print(output)
    print('prediction is', output)
    # showing the prediction results in a UI
    return render_template('result2.html',prediction_text=output)

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
    #app.run(debug=False) # running the app
    app.run('0.0.0.0',8080) #local host 8080