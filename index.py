import json
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bm25_worker import Document, BM25Query, BM25
from pymongo import MongoClient


bm25_instance = BM25()

app = Flask(__name__)

# Configure MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/bm25'
mongo = PyMongo(app)

client = MongoClient('mongodb://localhost:27017/bm25')

@app.route('/')
def hello():
    return 'Hello, this is your Flask server!'

@app.route('/search', methods=['POST'])
def get_data_from_mongodb():
    try:
        data_received=request.get_json()
        phrase = data_received.get('phrase')
        index = data_received.get('index')
        # Connect to MongoDB and retrieve data #pass in index you are searching
        db = client.get_database()
        collection = db[index]
        data = collection.find()
        result = [{"content": doc["content"], "filename": doc["filename"], "size": doc["metadata"]["size"]} for doc in data]
        # print(result)

        # result = json.loads(result)
        for doc_data in result:
          numeric_part = ''.join(char for char in doc_data["filename"] if char.isdigit())
          filename_int = int(numeric_part)
          doc = Document(
            id=filename_int,
            text=doc_data["content"]
          )
          # print(doc)
          bm25_instance.add_document(doc)
        print(bm25_instance._docs)
        query = BM25Query(
          phrase= phrase,
          max_results=5
        )
        resp = bm25_instance.search(query)
        return jsonify(resp)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)