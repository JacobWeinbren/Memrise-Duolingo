"""import requests, ujson

url = 'https://api.rosette.com/rest/v1/name-translation'
headers = {
    "X-RosetteAPI-Key": "a700fce28a5082960ceb2d3a44568ccf",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Cache-Control": "no-cache"
}

def transliterate(word):
    data = {
        "name": word, 
        "sourceScript": "Hebr",
        "sourceLanguageOfOrigin": "heb",
        "sourceLanguageOfUse": "heb",
        "targetLanguage": "eng", 
        "targetScript": "Latn",
        "targetScheme": "FOLK"
    }
    r = requests.post(url, data=ujson.dumps(data), headers=headers)
    return ujson.loads(r.text)['translation'].lower()


print(transliterate('אֲרוּחַת צָהֳרַיִם'))"""

import requests
import json
import uuid

# Define the API endpoint
endpoint = "https://api.cognitive.microsofttranslator.com/transliterate?api-version=3.0"

# Set up the header with your subscription key
subscription_key = "d7d3b8d876754dfc98f45da0792a922e"
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    "Ocp-Apim-Subscription-Region": "uksouth",
    'Content-Type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# Set up the parameters for the transliteration
params = {
    'language': 'he',
    'fromScript': 'Hebr',
    'toScript': 'Latn'
}

body = [{"Text":'אֲרוּחַת צָהֳרַיִם'}]

# Make the API request
response = requests.post(endpoint, headers=headers, params=params, json=body)

# Check status code
if response.status_code == 200:
    # Parse the response
    transliterations = response.json()

    # Print out the transliterations
    for transliteration in transliterations:
        print(transliteration['text'])
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)

