
**PRE-REQUISITES**
1. Mongodb installed and running
2. Create a db called bm25 in your mongo cli or change the name of the path to connect to the db in index.py lines 13 and 17

**BUILD SERVICE**
1. run the build_index script to transform the text files in the scrape folders in assets to serialized and indexed json files.
   `python3 build_index.py —data_folder=YOURDATA —output_index=OUTPUTINDEXFILENAME`
   eg: `python3 build_index.py --data_folder=scrape_0 --output_index=index_0`
2. a file should appear in the root directory with the name of the file you passed in as the output_index

**SEARCH SERVICE**
1. run the Flask server to start the server
   `python3 index.py`
2. run the search_service, passing in the index you'd like to search and the search query
    `python3 search_service.py --phrase='what is gravity' --index='index_0'`
3. this will return an object with a key "documents" and a value that is an array of objects. Each object in the array has an "id" which references a the txt filename in the original scrape file and "text" which is the text from that file that most closely matches your search query.
4. 
