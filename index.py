import json
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from search_service import Document, BM25Query, BM25


bm25_instance = BM25()

app = Flask(__name__)

# Configure MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/bm25'
mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'Hello, this is your Flask server!'

@app.route('/search')
def get_data_from_mongodb():
    try:
        # Connect to MongoDB and retrieve data
        collection = mongo.db.index_0
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
          phrase= 'how big is a black hole',
          max_results=5
        )
        resp = bm25_instance.search(query)
        print('resp', resp)
        return jsonify(resp)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/search')
# def search_data_from_mongodb():
#   try:
#       #get all data in index from mongodb
#       collection = mongo.db.index_0
#       data = collection.find()
#       result = [{"content": doc["content"], "filename": doc["filename"], "size": doc["metadata"]["size"]} for doc in data]
#       #create a doc for every entry in collection
#       for doc_data in result:
#         numeric_part = ''.join(char for char in doc_data["filename"] if char.isdigit())
#         filename_int = int(numeric_part)
#         doc = Document(
#           id=filename_int,
#           text=doc_data["content"]
#         )
#         print(doc)
#       #create a dataframe of all the docs
#         bm25_instance.add_document(doc)
#       #call search with query
#       query = BM25Query('wormhole', 5)
#       bm25_instance.search(query)
#    except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)