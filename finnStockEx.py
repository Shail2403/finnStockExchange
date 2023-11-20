import requests
import pymongo
import toml

config = toml.load("data.toml")

client = pymongo.MongoClient(config['mongodb']['uri'])
db = client[config['mongodb']['database_name']]
collection = db[config['mongodb']['symbols_collection']] 

api_url = config['finnhub']['api_url']
api_key = config['finnhub']['api_key']

headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    api_data = response.json()  

    if isinstance(api_data, list):
        collection.insert_many(api_data)
        print("Data has been successfully stored in MongoDB.")
    elif isinstance(api_data, dict):
        data = api_data.get('data', [])
        if isinstance(data, list):
            collection.insert_many(data)
            print("Data has been successfully stored in MongoDB.")
        else:
            print("API response does not contain a valid data list.")
    else:
        print("API response format is not recognized.")
else:
    print("Failed to fetch data from the API. Status code:", response.status_code)

client.close()
