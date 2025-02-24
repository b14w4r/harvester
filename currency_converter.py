import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ['API_KEY']
url = "https://api.currencyapi.com/v3/historical"
headers = {
    'apikey': API_KEY,
}


def conversion(date, currency):
    try:
        response = requests.request("GET", url, headers=headers,params={
            'base_currency':'RUB',
            'currencies': currency,
            'date':date})

        return float(response.json()['data'][currency]['value'])
    except Exception as e:
        print(e)
        return 1.0
