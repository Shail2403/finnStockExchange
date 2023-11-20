from flask import Flask, request, jsonify
import pymongo
import toml

config = toml.load("data.toml")

app = Flask(__name__)

client = pymongo.MongoClient(config['mongodb']['uri'])
db = client[config['mongodb']['database_name']]
collection = db[config['mongodb']['uids_collection']]

@app.route('/', methods=['GET', 'POST'])
def uids():
    try:
        data = request.get_json()
        if data:
            if 'first_name' in data and 'last_name' in data and 'email' in data and 'phone_number' in data:
                collection.insert_one(data)
                return jsonify({"message": "Data has been successfully stored in MongoDB."})
            else:
                return jsonify({"error": "Incomplete data. Required fields: first_name, last_name, email, phone_number"})
        else:
            return jsonify({"error": "No data received."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port=5001) 
