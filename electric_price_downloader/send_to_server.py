import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

def send_to_server():
    #key = os.getenv("API_TOKEN")
    url = "http://localhost:3001/api/fiprice/upload?apikey=aatestbb"

    with open('data/output_FI_DayAheadPrices.json', 'r') as fp:
        priceRows = json.load(fp)
    print(priceRows)
    r = requests.post(url, json=priceRows)
    print(r)
