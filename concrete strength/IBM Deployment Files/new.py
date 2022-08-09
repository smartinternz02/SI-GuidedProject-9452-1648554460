import requests


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account
API_KEY = "SIWh-3Wte2pfbwYHOWKw_VRXA1OdfH7rYkBBI9YEqjnT"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": ["cement", "slag", "ash", "Water", "superplastic", "coarseagg", "fineagg", "age"],
                                   "values": [[35, 45, 56, 26, 36, 45, 30, 25]]}]}

response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e32379f4-c48c-41d1-ad13-eff9b2a4d38e/predictions?version=2022-07-29", json=payload_scoring,
 headers ={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
pred= response_scoring.json()
print(pred)
output= pred['predictions'][0]['values'][0][0]
print(output)
