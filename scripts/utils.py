import requests
import pandas as pd
import datetime
import os
import json
from datetime import datetime
import time

GFD_API_URL = "https://api.globalfinancialdata.com"

def writeJSONToFile(fileSuffix, jsonContents):
    now = datetime.now()
    jsonFilename = now.strftime("%Y%m%d-%H%M%S%f") + '_' + fileSuffix +'.json'
    relativeDirectory = './responses/'
    if not os.path.isdir(relativeDirectory):
        os.mkdir(relativeDirectory)
    outputfilepath = relativeDirectory + jsonFilename
    with open(outputfilepath,'w') as f:
        json.dump(jsonContents, f)

MAX_RETRIES = 3  # Number of retry attempts
RETRY_DELAY = 2  # Initial delay in seconds for exponential backoff

def call_api(path, parameters):
    url = GFD_API_URL + path
    headers = {'Content-type': 'application/json'}
    attempt = 0

    while attempt < MAX_RETRIES:
        print("Attempt %d: calling %s" % (attempt + 1, url))
        print("Request body:\n %s" % parameters)
        writeJSONToFile(path.strip('/') + 'Request', parameters)

        try:
            resp = requests.post(url, headers=headers, data=json.dumps(parameters))

            # Check if the response is successful
            if resp.status_code == 200:
                return resp
            else:
                print("API call failed with status code %s" % resp.status_code)
                print("API call failed with response %s" % resp.text)

        except requests.exceptions.RequestException as e:
            print("Request failed with exception: %s" % e)

        # Increment the attempt counter
        attempt += 1
        # Exponential backoff: double the delay after each attempt
        time.sleep(RETRY_DELAY * (2 ** (attempt - 1)))

    # If we exhaust all attempts, return the last response or raise an error
    print("All retry attempts exhausted. API call failed.")
    return None


def gfd_auth(username, password):
    parameters = {'username': username, 'password': password}
    resp = call_api('/login', parameters=parameters)

    #check for unsuccessful API returns
    if resp.status_code != 200:
        raise ValueError('GFD API request failed with HTTP status code %s' % resp.status_code)

    json_content = resp.json()
    print("GFD API token recieved at %s" % str(datetime.now()))
    return json_content

def gfd_series(token, **kwargs):
    seriesId = kwargs.get('seriesId',None)
    seriesName = kwargs.get('seriesName',None)
    splitAdjusted = kwargs.get('splitAdjusted',None)
    startDate = kwargs.get('startDate',None)
    endDate = kwargs.get('endDate',None)
    periodicity = kwargs.get('periodicity',None)
    closeOnly = kwargs.get('closeOnly',None)
    currency = kwargs.get('currency',None)
    inflationAdjusted = kwargs.get('inflationAdjusted',None)
    annualFlow = kwargs.get('annualFlow',None)
    totalReturn = kwargs.get('totalReturn',None)
    corporateActions = kwargs.get('corporateActions',None)
    metadata = kwargs.get('metadata',None)
    incFields = kwargs.get('incFields',None)
    includeAverage = kwargs.get('includeAverage',None)
    periodPercentChange = kwargs.get('periodPercentChange',None)
    parameters = {'token': token,
                  "seriesId": seriesId,
                  "seriesName": seriesName,
                  "splitAdjusted": splitAdjusted,
                  "startDate": startDate,
                  "endDate": endDate,
                  "periodicity": periodicity,
                  "closeOnly": closeOnly,
                  "currency": currency,
                  "inflationAdjusted": inflationAdjusted,
                  "annualFlow": annualFlow,
                  "totalReturn": totalReturn,
                  "corporateActions": corporateActions,
                  "metadata": metadata,
                  "incFields": incFields,
                  "includeAverage": includeAverage,
                  "periodPercentChange": periodPercentChange
                  }

    parameters = {key:val for key, val in parameters.items() if val != None}
    r = call_api('/series', parameters=parameters)
    if r is None:
        return None
    series_data = r.json()
    return series_data

def save_series_to_csv(token, seriesName, periodicity, fileNameOut):
    series_price_data = gfd_series(token, seriesName=seriesName, periodicity=periodicity)
    # series_price_data = series_info["price_data"]
    # writeJSONToFile('series_price_data', series_price_data)
    if series_price_data is None:
        return
    data = pd.DataFrame(series_price_data['price_data'])
    data['symbol'] = seriesName
    data.to_csv(fileNameOut + '.csv')