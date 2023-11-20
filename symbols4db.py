import requests
from pymongo import MongoClient
import toml

config = toml.load("data.toml")

mongo_uri = config['mongodb']['uri']
database_name = config['mongodb']['database_name']
collection_name = config['mongodb']['earnings_collection']

def fetch_and_insert_data(symbol, collection):
    alpha_vantage_url = config['alpha_vantage']['url']
    function = "EARNINGS"
    api_key = config['alpha_vantage']['api_key']

    params = {
        'function': function,
        'symbol': symbol,
        'apikey': api_key
    }

    response = requests.get(alpha_vantage_url, params=params)
    data = response.json()

    collection.insert_one({
        'symbol': symbol,
        'data': data
    })

symbols = ["DE", "AAPL", "MSFT", "BKH"]
collection = MongoClient(mongo_uri)[database_name][collection_name]

for symbol in symbols:
    fetch_and_insert_data(symbol, collection)
